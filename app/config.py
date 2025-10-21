from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "String Analysis API"
    app_version: str = "1.0.0"
    debug: bool = False
    rate_limit: int = 100
    rate_limit_window: int = 3600  # 1 hour in seconds
    
    class Config:
        env_file = ".env"

settings = Settings()