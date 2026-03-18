from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """конфиг - модель pydantic"""

    # postgresql
    POSTGRES_HOST: str = Field("localhost", validation_alias="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, validation_alias="POSTGRES_PORT")
    POSTGRES_USER: str = Field("postgres", validation_alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", validation_alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("test_db", validation_alias="POSTGRES_DB")

    # redis
    REDIS_HOST: str = Field("localhost", validation_alias="REDIS_HOST")
    REDIS_PORT: int = Field(6379, validation_alias="REDIS_PORT")
    REDIS_DB: int = Field(0, validation_alias="REDIS_DB")

    # общие настройки
    APP_NAME: str = Field("Test Service", validation_alias="APP_NAME")
    DEBUG: bool = Field(False, validation_alias="DEBUG")
    LOG_LEVEL: str = Field("INFO", validation_alias="LOG_LEVEL")

    @property
    def database_url(self) -> str:
        """сборка результирующего sql url"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def redis_url(self) -> str:
        """сборка результирующего redis url"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
