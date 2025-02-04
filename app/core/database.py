from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import create_engine, text
from app.core.settings import settings
from app.models import Base
from typing import AsyncGenerator, Any


DATABASE_URL = URL.create(
    drivername=f"{settings.db_dialect}+{settings.db_driver}",
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_database,
)

DATABASE_URL_ASYNC = URL.create(
    drivername=f"{settings.db_dialect}+{settings.db_driver_async}",
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_database,
)

# Create an async engine to connect to the database
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=settings.db_logging)

# Session configuration to manage DB connections
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)


# Dependency to get the database session
async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as db:
        yield db


def setup_database():
    engine = create_engine(DATABASE_URL, echo=settings.db_logging)
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text(
                    f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{settings.db_database}'"
                )
            )
            tables = result.scalars().all()
            if len(tables) == 0:
                print("Creating tables...")
                Base.metadata.create_all

        print("✅ Database setup complete!")
        print("Connected to MySQL database at:", settings.db_host)
        print("Database:", settings.db_database)
        print("Tables:", tables)
    except Exception as e:
        print("❌ Database setup failed:", e)
    finally:
        engine.dispose()
