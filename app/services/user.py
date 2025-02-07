from sqlalchemy.ext.asyncio import AsyncSession
from app.repos.user import UserRepository
from app.repos.role import RoleRepository
from app.repos.sso import SSORepository
from app.schemas import (
    UserBase,
    UserModel,
    UserUpdate,
    SSOModel,
)
from typing import Optional


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

        existing_user = (
            await UserRepository.get_by_username(db, user_data.username)
            if user_data.username
            else None
        )
        if existing_user:
            raise ValueError(f"User with username {user_data.username} already exists")

        user = await UserRepository.create(db, user_data)
        user = await UserService.assign_role(db, user.id, "employee")
        return UserModel.model_validate(user)

    @staticmethod
    async def create_sso(db: AsyncSession, sso_data: SSOModel) -> SSOModel:
        """Create a new SSO entry in the database."""
        sso = await SSORepository.create(db, sso_data)
        return SSOModel.model_validate(sso)

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
    async def revoke_role(db: AsyncSession, user_id: str, role_name: str) -> UserModel:
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
    async def list_users(db: AsyncSession) -> list[UserModel]:
        """List all users in the database."""
        users = await UserRepository.list(db)
        return [UserModel.model_validate(user) for user in users]

    @staticmethod
    async def list_sso_by_user_id(db: AsyncSession, user_id: str) -> list[SSOModel]:
        """List all SSO entries for a specific user."""
        sso_entries = await SSORepository.list_by_user_id(db, user_id)
        return [SSOModel.model_validate(sso) for sso in sso_entries]

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
        user = await UserRepository.get_by_id(db, sso.user_id) if sso else None
        return UserModel.model_validate(user) if user else None

    @staticmethod
    async def get_sso_by_user_provider(
        db: AsyncSession, user_id: str, provider: str
    ) -> Optional[SSOModel]:
        """Retrieve an SSO entry by provider and provider UID."""
        sso = await SSORepository.get_by_user_id_and_provider(db, user_id, provider)
        return SSOModel.model_validate(sso) if sso else None

    @staticmethod
    async def get_sso_by_provider_sub(
        db: AsyncSession, provider: str, sub: str
    ) -> Optional[SSOModel]:
        """Retrieve an SSO entry by provider and provider UID."""
        sso = await SSORepository.get_by_provider_and_sub(db, provider, sub)
        return SSOModel.model_validate(sso) if sso else None

    @staticmethod
    async def update_user(
        db: AsyncSession, user_id: str, updates: UserUpdate
    ) -> UserModel:
        """Update user details."""
        user = await UserRepository.update(db, user_id, updates)
        return UserModel.model_validate(user)

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: str) -> bool:
        """Delete a user by their ID."""
        return await UserRepository.delete(db, user_id)

    @staticmethod
    async def delete_sso(db: AsyncSession, user_id: str, provider: str) -> bool:
        """Delete an SSO entry by user ID and provider."""
        return await SSORepository.delete(db, user_id, provider)
