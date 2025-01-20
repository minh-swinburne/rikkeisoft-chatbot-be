from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import RoleBase, RoleModel
from app.models import Role
from app.repos import _commit_and_refresh
from typing import Optional


class RoleRepository:
    @staticmethod
    async def create(
        db: AsyncSession, role_data: RoleBase
    ) -> Role:
        """
        Create a new role.
        """
        role = Role(name=role_data.name, description=role_data.description)
        db.add(role)
        return await _commit_and_refresh(db, role)

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Optional[Role]:
        """
        Retrieve a role by its name.
        """
        result = await db.execute(select(Role).where(Role.name == name))
        return result.scalars().first()

    @staticmethod
    async def list(db: AsyncSession) -> list[Role]:
        """
        List all roles.
        """
        result = await db.execute(select(Role))
        return result.scalars().all()

    @staticmethod
    async def delete(db: AsyncSession, role_id: int) -> bool:
        """
        Delete a role by its ID.
        """
        role = await db.get(Role, role_id)
        if not role:
            return False
        try:
            await db.delete(role)
            await db.commit()
            return True
        except:
            await db.rollback()
            raise
