"""# core/config.py -> centralizes environment-based configuration and prevents hard-coding secrets


# Old (Pydantic v1)
# from pydantic import BaseSettings

# New (Pydantic v2)
from pydantic_settings import BaseSettings

# BaseSettings -> allows loading settings from environment variables or a .env file
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Instantiate settings to be used throughout the application
settings = Settings()"""

from pydantic_settings import BaseSettings

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
