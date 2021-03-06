from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str
    sqlalchemy_base_url: str
    sqlalchemy_check_same_thread: bool
    sqlalchemy_expire_on_commit: bool
    sqlalchemy_autocommit: bool
    sqlalchemy_autoflush: bool
    drop_all_tables_on_startup: bool
    jwt_signature_secret: str
    jwt_encryption_secret: str
    jws_algo: str
    jwe_algo: str
    jwe_encryption: str

    class Config:
        env_file = '../.env'


@lru_cache()
def get_settings() -> Settings:
    return Settings()   # type: ignore
