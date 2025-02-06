from sqlalchemy.ext.asyncio import AsyncSession
from app.repos.user import UserRepository
from app.core.settings import settings
from app.utils import parse_timedelta
from app.schemas import UserModel, TokenBase, TokenModel, AuthModel
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone
from typing import Optional


class AuthService:
    """
    Handles business logic for authentication and token management.
    """

    @staticmethod
    def create_access_token(auth_data: TokenBase) -> str:
        """Create an access token for a user."""
        expires_delta = parse_timedelta(settings.jwt_access_expires_in)

        # Define token claims (payload)
        payload = {
            "sub": auth_data.sub,  # Subject
            "email": auth_data.email,  # Optional claim
            "firstname": auth_data.firstname,  # Optional claim
            "lastname": auth_data.lastname,  # Optional
            "username": auth_data.username,  # Optional claim
            "avatar_url": auth_data.avatar_url,  # Optional claim
            "provider": auth_data.provider,  # Optional claim
            "roles": auth_data.roles,  # Optional claim
            "type": "access",  # Custom claim
            "iat": datetime.now(timezone.utc),  # Issued at
            "exp": datetime.now(timezone.utc) + expires_delta,  # Expiration time
        }

        return jwt.encode(
            payload, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )

    @staticmethod
    def create_refresh_token(sub: str) -> str:
        """Create a refresh token for a user."""
        expires_delta = parse_timedelta(settings.jwt_refresh_expires_in)

        # Define token claims (payload)
        payload = {
            "sub": sub,  # Subject
            "type": "refresh",  # Custom claim
            "iat": datetime.now(),  # Issued at
            "exp": datetime.now() + expires_delta,  # Expiration time
        }

        return jwt.encode(
            payload, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
        )

    @staticmethod
    def grant_access(user: UserModel, provider: str = "") -> AuthModel:
        """Generate access and refresh tokens for a user."""
        roles = list(map(lambda role: role.name, user.roles))
        auth_data = TokenBase(
            sub=user.id,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            avatar_url=user.avatar_url,
            provider=provider,
            roles=roles,
        )
        access_token = AuthService.create_access_token(auth_data)
        refresh_token = AuthService.create_refresh_token(user.id)

        return AuthModel.model_validate(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }
        )

    @staticmethod
    def validate_token(token: str) -> TokenModel:
        """Validate a JWT token and return its payload."""
        try:
            # print("Validating token:", token)
            payload = jwt.decode(
                token, key=settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
            )
            return TokenModel.model_validate(payload)
        except ExpiredSignatureError:
            raise ValueError("Token expired")
        except JWTError:
            raise ValueError("Invalid token")

    @staticmethod
    async def refresh_token(db: AsyncSession, refresh_token: str) -> str:
        """Refresh an access token using a refresh token."""
        payload = AuthService.validate_token(refresh_token)
        if payload["type"] != "refresh":
            raise ValueError("Invalid token type")

        user = await UserRepository.get_by_id(db, payload["sub"])
        if not user:
            raise ValueError("User not found")

        auth_data = TokenBase(
            sub=user.id,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            avatar_url=user.avatar_url,
            roles=user.roles,
        )
        return AuthService.create_access_token(auth_data)
