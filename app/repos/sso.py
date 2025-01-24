from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.sso import SSOModel
from app.models.sso import SSO
from app.repos import _commit_and_refresh
from typing import Optional


class SSORepository:
    @staticmethod
    async def create(db: AsyncSession, sso_data: SSOModel) -> SSO:
        """
        Create a new SSO entry.
        """
        sso = SSO(
            user_id=sso_data.user_id,
            provider=sso_data.provider,
            sub=sso_data.sub,
        )
        db.add(sso)
        return await _commit_and_refresh(db, sso)

    @staticmethod
    async def list_by_user_id(db: AsyncSession, user_id: str) -> list[SSO]:
        """
        List all SSO entries for a specific user.
        """
        result = await db.execute(select(SSO).where(SSO.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def get_by_user_id_and_provider(
        db: AsyncSession, user_id: str, provider: str
    ) -> Optional[SSO]:
        """
        Get an SSO entry by user ID and provider.
        """
        result = await db.execute(
            select(SSO).where(SSO.user_id == user_id, SSO.provider == provider)
        )
        return result.scalars().first()

    @staticmethod
    async def get_by_provider_and_sub(
        db: AsyncSession, provider: str, sub: str
    ) -> Optional[SSO]:
        """
        Get an SSO entry by provider and sub.
        """
        result = await db.execute(
            select(SSO).where(SSO.provider == provider, SSO.sub == sub)
        )
        return result.scalars().first()

    @staticmethod
    async def delete(db: AsyncSession, user_id: str, provider: str) -> bool:
        """
        Delete an SSO entry by user ID and provider.
        """
        sso_entry = await db.get(SSO, (user_id, provider))
        if not sso_entry:
            return False
        try:
            await db.delete(sso_entry)
            await db.commit()
        except:
            await db.rollback()
            raise
        return True
