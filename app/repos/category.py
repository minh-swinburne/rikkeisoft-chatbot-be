from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repos import _commit_and_refresh
from app.models import Category
from app.schemas import CategoryBase


class CategoryRepository:
    @staticmethod
    async def create(db: AsyncSession, category_data: CategoryBase) -> Category:
        category = Category(**category_data.model_dump())
        db.add(category)
        return await _commit_and_refresh(db, category)

    @staticmethod
    async def list(db: AsyncSession) -> list[Category]:
        result = await db.execute(select(Category))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, category_id: str) -> Category:
        return await db.get(Category, category_id)

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Category:
        result = await db.execute(select(Category).where(Category.name == name))
        return result.scalars().first()

    @staticmethod
    async def update(
        db: AsyncSession, category_id: str, updates: CategoryBase
    ) -> Category:
        category = await CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} not found.")

        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(category, key, value)

        return await _commit_and_refresh(db, category)

    @staticmethod
    async def delete(db: AsyncSession, category_id: str) -> bool:
        category = await CategoryRepository.get_by_id(db, category_id)
        if not category:
            return False

        db.delete(category)
        await db.commit()
        return True
