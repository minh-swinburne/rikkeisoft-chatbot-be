from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

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
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# Dependency to get the database session
async def get_db():
    async with async_session() as db:
        yield db
