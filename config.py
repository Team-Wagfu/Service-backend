# Wagfu service backend
# common configuration and settings, fastapi friendly
# Update 12 May 2026

# load cloud or local configuration based on the IS_CLOUD env

from os import getenv
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url


class Config(BaseSettings):
    """Settings instance, holds all configuration values"""

    # db configurations
    DB_DRIVERNAME: Optional[str] = None
    DB_USERNAME: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_DATABASE: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_INTERNAL_STRING: Optional[str] = None

    # security
    JWT_SECRET: Optional[str] = None

    # path configurations
    DATA_ROOT: Optional[str] = None
    PROJECT_ROOT: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env.prod" if int(getenv("IS_CLOUD", "0")) else ".env.local"
    )

    @property
    def url(self):
        """return the appropriate type of url"""
        if int(getenv("IS_CLOUD", "0")):
            url = make_url(self.DB_INTERNAL_STRING)
        else:
            url = URL.create(
                drivername="postgresql+psycopg",
                username=self.DB_USERNAME,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                database=self.DB_DATABASE,
            )
        return url


config = Config()

__all__ = ["config"]
