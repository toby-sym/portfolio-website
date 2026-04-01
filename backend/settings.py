from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database (REQUIRED - set DATABASE_URL in .env)
    database_url: str
    
    # JWT (REQUIRED - set SECRET_KEY in .env for production)
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    
    # Admin credentials (CHANGE THESE in .env production!)
    admin_username: str = "admin"
    admin_password: str = "admin"
    
    # CORS - Restrict to specific origins in production
    # Format: ["http://localhost:5173", "https://example.com"]
    cors_origins: list = ["http://localhost:5173", "https://toby-sym.github.io"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
