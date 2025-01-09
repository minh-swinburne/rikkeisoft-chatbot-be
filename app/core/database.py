from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+aiomysql://root:0Kcbctmbskn!@localhost/rikkeisoft-intern"

# Create async engine for the database connection
engine = create_async_engine(DATABASE_URL, echo=True)

# Session configuration to manage DB connections
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to get the database session
async def get_db():
    async with async_session() as session:
        yield session