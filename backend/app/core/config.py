from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Q&A Platform"
    VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str
    DEBUG: str
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS (comma-separated string, same as Photo system)
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_list(self) -> List[str]:
        """Convert comma-separated CORS to list."""
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
