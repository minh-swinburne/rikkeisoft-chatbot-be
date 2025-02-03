from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.settings import settings
from typing import AsyncGenerator, Any


DATABASE_URL = URL.create(
    drivername=f"{settings.db_dialect}+{settings.db_driver}",
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_database,
)

# Create async engine for the database connection
engine = create_async_engine(DATABASE_URL, echo=False)

# Session configuration to manage DB connections
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# Dependency to get the database session
async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as db:
        yield db


def setup_database():
    from sqlalchemy import text
    from app.models import Base
    import asyncio

    async def create_tables():
        try:
            async with engine.begin() as conn:
                result = await conn.execute(
                    text(
                        f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{settings.db_database}'"
                    )
                )
                tables = result.scalars().all()
                if len(tables) == 0:
                    print("Creating tables...")
                    await conn.run_sync(Base.metadata.create_all)
            print("✅ Database setup complete!")
            print("Connected to MySQL database at:", settings.db_host)
            print("Database:", settings.db_database)
            print("Tables:", tables)
        except Exception as e:
            print("❌ Database setup failed:", e)

    asyncio.create_task(create_tables())
