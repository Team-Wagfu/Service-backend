# Wagfu service backend
# common configuration and settings, fastapi friendly
# Update 12 May 2026

from os import getenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, Engine, create_engine


class Config(BaseSettings):
    """common configuration class"""

    DB_USERNAME: str = "wagfu_admin"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_DATABASE: str = "wagfu_db"
    DB_PASSWORD: str  # will be populated by .env
    JWT_SECRET: str  # will be populated by .env

    model_config = SettingsConfigDict(env_file=".env.local")

    @property
    def url(self) -> URL:
        """construct and return the URL object"""
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_DATABASE,
        )

    @property
    def engine(self) -> Engine:
        """return the engine object"""
        return create_engine(
            self.url,
            echo=True,
        )


config = Config()

__all__ = ["config"]
