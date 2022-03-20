from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import get_settings

settings = get_settings()
engine = create_async_engine(settings.sqlalchemy_base_url, future=True)
