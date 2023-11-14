from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    database_url: str = Field(env="DATABASE_URL", default="sqlite:///database.db")


class Settings(BaseSettings):
    environment: str = Field(env="ENV", default="DEV")
    database: DatabaseSettings = DatabaseSettings()
