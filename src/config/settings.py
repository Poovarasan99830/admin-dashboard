from pydantic import BaseSettings, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "admin-dashboard-service"
    DATABASE_URL: PostgresDsn = "sqlite+aiosqlite:///./dev.db"  # change to postgres in production
    ADMIN_API_KEY: Optional[str] = "supersecretadminkey"  # simple placeholder

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
