from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


# Base = declarative_base()
class Base(DeclarativeBase, AsyncAttrs):
    pass
