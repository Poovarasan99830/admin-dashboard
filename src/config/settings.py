from pydantic import BaseSettings



class Settings(BaseSettings):
    PROJECT_NAME: str = "Admin Dashboard Service"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
