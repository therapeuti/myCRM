from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "CRM API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/instance/mycrm.db"
    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: Path = BASE_DIR / "instance" / "logs"
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "CRM API"
    API_DESCRIPTION: str = "Customer Relationship Management System API"
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

def get_settings() -> Settings:
    return settings
