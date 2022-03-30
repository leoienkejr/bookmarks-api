from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str | None
    sqlalchemy_base_url: str | None
    sqlalchemy_check_same_thread: bool | None
    sqlalchemy_expire_on_commit: bool | None
    sqlalchemy_autocommit: bool | None
    sqlalchemy_autoflush: bool | None
    drop_all_tables_on_startup: bool | None

    class Config:
        env_file = '../.env'


@lru_cache()
def get_settings() -> Settings:
    return Settings()   # type: ignore
