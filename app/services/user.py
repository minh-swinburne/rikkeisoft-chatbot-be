from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime
from app.core.config import settings
from app.utils import parse_timedelta
from app.models import User
import uuid


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str,
    firstname: str,
    lastname: str,
    admin: bool,
    provider: str,
    provider_uid: str,
) -> User:
    user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        password=pwd_context.hash(password),
        firstname=firstname,
        lastname=lastname,
        admin=admin,
        provider=provider,
        provider_uid=provider_uid,
        )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_provider_uid(db: AsyncSession, provider: str, provider_uid: str) -> User:
    stmt = select(User).where(User.provider == provider, User.provider_uid == provider_uid)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def list_users(db: AsyncSession):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()


async def authenticate_user(db: AsyncSession, username: str, password: str) -> User:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user and pwd_context.verify(password, user.password):
        return user
    return None


def create_access_token(
    sub: str,   # Subject / User ID
    # username: str,
    firstname: str,
    lastname: str,
    email: str,
    roles: list,
    provider: str,
):
    expires_delta = parse_timedelta(settings.jwt_access_expires_in)

    # Define token claims (payload)
    payload = {
        "sub": sub,  # Subject
        # "username": username,  # Optional claim
        "firstname": firstname,  # Optional claim
        "lastname": lastname,  # Optional
        "email": email,  # Optional claim
        "roles": roles,  # Optional claim
        "provider": provider,  # Optional claim
        "type": "access",  # Custom claim
        "iat": datetime.now(),  # Issued at
        "exp": datetime.now() + expires_delta,  # Expiration time
    }

    return jwt.encode(
        payload, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def create_refresh_token(sub: str):
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


def validate_token(token: str):
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
