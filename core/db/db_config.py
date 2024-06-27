import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine


class Settings:
    DB_HOST: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: str

    def __init__(self):
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_USERNAME = os.getenv('DB_USERNAME')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_PORT = os.getenv('DB_PORT')

    @property
    def database_url_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def database_url_psycopg(self):
        return f'postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
engine_async = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=False
)

engine_sync = create_engine(
    url=settings.database_url_psycopg,
    echo=False
)