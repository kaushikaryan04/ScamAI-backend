from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    APP_NAME: str = "ScamAI MongoDB App"
    DEBUG_MODE: bool = True

    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    APP_SECRET_KEY: str
    MONGODB_URL: str
    MONGODB_DB_NAME: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
