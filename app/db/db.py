from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import Settings, get_settings


settings: Settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.sqlalchemy_base_url, future=True,
    connect_args={'check_same_thread': settings.sqlalchemy_check_same_thread})

SessionLocal = sessionmaker(bind=engine,
                            expire_on_commit=settings.sqlalchemy_expire_on_commit,
                            autocommit=settings.sqlalchemy_autocommit,
                            autoflush=settings.sqlalchemy_autoflush,
                            class_=AsyncSession)

Base = declarative_base()
