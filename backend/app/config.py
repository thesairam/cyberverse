from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    APP_NAME: str = "CyberVerse Intelligence Aggregator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "postgresql+asyncpg://cyberverse:cyberverse@localhost:5432/cyberverse"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:1337"]
    COLLECT_INTERVAL_MINUTES: int = 15
    FINANCIAL_INTERVAL_MINUTES: int = 60
    YOUTUBE_API_KEY: str = ""
    NEWSAPI_KEY: str = ""
    ALPHA_VANTAGE_KEY: str = ""
    CRUNCHBASE_API_KEY: str = ""
    SENTIMENT_MODEL: str = "vader"
    DEFAULT_TIMEZONE: str = "UTC"


@lru_cache
def get_settings() -> Settings:
    return Settings()
