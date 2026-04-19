import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = "sk-or-placeholder"
    OPENROUTER_MODEL: str = "mistralai/mistral-7b-instruct"
    BACKEND_URL: str = "http://localhost:8000"
    REDIS_URL: str = "redis://localhost:6379"
    TAVILY_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
