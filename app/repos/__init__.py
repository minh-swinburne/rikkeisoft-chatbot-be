from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

async def _commit_and_refresh(db: AsyncSession, obj: object) -> object:
    """Helper method to commit changes and refresh the object."""
    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except SQLAlchemyError:
        await db.rollback()
        raise