from sqlalchemy.ext.asyncio import AsyncSession
from app.repos.user import UserRepository
from app.repos.role import RoleRepository
from app.repos.sso import SSORepository
from app.core.config import settings
from app.utils import parse_timedelta
from app.schemas import UserBase, UserModel, UserUpdate, SSOBase, AuthBase, AuthModel
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime
from typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    Handles business logic for user management, including CRUD operations, authentication, and token generation.
    """
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserBase) -> UserModel:
        """Create a new user in the database."""
        existing_user = await UserRepository.get_by_email(db, user_data.email)
        if existing_user:
            raise ValueError(f"User with email {user_data.email} already exists")

        existing_user = await UserRepository.get_by_username(db, user_data.username)
        if existing_user:
            raise ValueError(f"User with username {user_data.username} already exists")

        user = await UserRepository.create(db, user_data)
        return UserModel.model_validate(user)

    @staticmethod
    async def assign_role(db: AsyncSession, user_id: str, role_name: str) -> UserModel:
        """Assign a role to a user."""
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")

        role = await RoleRepository.get_by_name(db, role_name)
        if not role:
            raise ValueError("Role not found")

        if role not in user.roles:
            user.roles.append(role)
            await db.commit()
            await db.refresh(user)

        return user

    @staticmethod
    async def remove_role(db: AsyncSession, user_id: str, role_name: str) -> UserModel:
        """Remove a role from a user."""
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")

        role = await RoleRepository.get_by_name(db, role_name)
        if not role:
            raise ValueError("Role not found")

        if role in user.roles:
            user.roles.remove(role)
            await db.commit()
            await db.refresh(user)

        return user

    @staticmethod
    async def create_sso(db: AsyncSession, sso_data: SSOBase) -> SSOBase:
        """Create a new SSO entry in the database."""
        sso = await SSORepository.create(db, sso_data)
        return SSOBase.model_validate(sso)

    @staticmethod
    async def list_users(db: AsyncSession) -> list[UserModel]:
        """List all users in the database."""
        users = await UserRepository.list(db)
        return [UserModel.model_validate(user) for user in users]

    @staticmethod
    async def list_sso_by_user_id(db: AsyncSession, user_id: str) -> list[SSOBase]:
        """List all SSO entries for a specific user."""
        sso_entries = await SSORepository.list_by_user_id(db, user_id)
        return [SSOBase.model_validate(sso) for sso in sso_entries]

    @staticmethod
    async def list_user_roles(db: AsyncSession, user_id: str) -> list[str]:
        """List all roles assigned to a user."""
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")

        return [role.name for role in user.roles]

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[UserModel]:
        """Retrieve a user by their ID."""
        user = await UserRepository.get_by_id(db, user_id)
        return UserModel.model_validate(user) if user else None

    @staticmethod
    async def get_user_by_username(
        db: AsyncSession, username: str
    ) -> Optional[UserModel]:
        """Retrieve a user by their username."""
        user = await UserRepository.get_by_username(db, username)
        # print(user.__dict__)
        return UserModel.model_validate(user) if user else None

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[UserModel]:
        """Retrieve a user by their email."""
        user = await UserRepository.get_by_email(db, email)
        return UserModel.model_validate(user) if user else None

    @staticmethod
    async def get_user_by_provider_sub(
        db: AsyncSession, provider: str, sub: str
    ) -> Optional[UserModel]:
        """Retrieve a user by their provider and provider UID."""
        sso = await SSORepository.get_by_provider_and_sub(db, provider, sub)
        user = await UserRepository.get_by_id(db, sso.user_id)
        return UserModel.model_validate(user) if user else None

    @staticmethod
    async def update_user(
        db: AsyncSession, user_id: str, updates: UserUpdate
    ) -> Optional[UserModel]:
        """Update user details."""
        user = await UserRepository.update(db, user_id, updates)
        return UserModel.model_validate(user) if user else None

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: str) -> bool:
        """Delete a user by their ID."""
        return await UserRepository.delete(db, user_id)

    @staticmethod
    async def delete_sso(db: AsyncSession, user_id: str, provider: str) -> bool:
        """Delete an SSO entry by user ID and provider."""
        return await SSORepository.delete(db, user_id, provider)

    @staticmethod
    def create_access_token(auth_data: AuthBase) -> str:
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
            "roles": auth_data.roles,  # Optional claim
            "type": "access",  # Custom claim
            "iat": datetime.now(),  # Issued at
            "exp": datetime.now() + expires_delta,  # Expiration time
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
    def grant_access(user: UserModel) -> AuthModel:
        """Generate access and refresh tokens for a user."""
        roles = list(map(lambda role: role.name, user.roles))
        auth_data = AuthBase(
            sub=user.id,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            avatar_url=user.avatar_url,
            roles=roles,
        )
        access_token = UserService.create_access_token(auth_data)
        refresh_token = UserService.create_refresh_token(user.id)

        return AuthModel.model_validate({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        })

    @staticmethod
    def validate_token(token: str) -> dict:
        """Validate a JWT token and return its payload."""
        try:
            payload = jwt.decode(
                token,
                key=settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm]
            )
            return payload
        except JWTError:
            raise ValueError("Invalid token")
        except ExpiredSignatureError:
            raise ValueError("Token expired")

    @staticmethod
    async def refresh_token(db: AsyncSession, refresh_token: str) -> str:
        """Refresh an access token using a refresh token."""
        payload = UserService.validate_token(refresh_token)
        if payload["type"] != "refresh":
            raise ValueError("Invalid token type")

        user = await UserRepository.get_by_id(db, payload["sub"])
        if not user:
            raise ValueError("User not found")

        auth_data = AuthBase(
            sub=user.id,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            avatar_url=user.avatar_url,
            roles=user.roles,
        )
        return UserService.create_access_token(auth_data)
