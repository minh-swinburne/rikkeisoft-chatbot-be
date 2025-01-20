from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import UserBase
from app.models import User
from app.repos import _commit_and_refresh
from datetime import datetime
from typing import Optional
import uuid


class UserRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        user_data: UserBase,
    ) -> User:
        """
        Create a new user.
        """
        user = User(
            id=str(uuid.uuid4()),
            **user_data.model_dump(),
            username_last_changed=datetime.now(),
        )
        db.add(user)
        return await _commit_and_refresh(db, user)

    @staticmethod
    async def list(db: AsyncSession) -> list[User]:
        """
        List all users.
        """
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.
        """
        return await db.get(User, user_id)

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.
        """
        if not username:
            raise ValueError("Username cannot be empty.")
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    @staticmethod
    async def update_username(
        db: AsyncSession, user_id: str, new_username: str
    ) -> User:
        """
        Update a user's username. Ensures the username is valid.
        """
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found.")
        if not new_username:
            raise ValueError("Username cannot be empty.")
        user.username = new_username
        user.username_last_changed = datetime.now()
        return await _commit_and_refresh(db, user)

    @staticmethod
    async def delete(db: AsyncSession, user_id: str) -> bool:
        """
        Delete a user by their ID.
        """
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            return False
        try:
            await db.delete(user)
            await db.commit()
            return True
        except:
            await db.rollback()
            raise
