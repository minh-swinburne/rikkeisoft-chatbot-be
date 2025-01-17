from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
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
engine = create_async_engine(DATABASE_URL, echo=True)

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
