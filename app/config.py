from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "String Analysis API"
    app_version: str = "1.0.0"
    debug: bool = False
    rate_limit: int = 100
    rate_limit_window: int = 3600  # 1 hour in seconds
    PORT: int = 8001
    HOST: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()