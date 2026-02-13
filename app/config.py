"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass

import dotenv

dotenv.load_dotenv()


@dataclass
class DatabaseConfig:
    """SQLite database configuration."""

    path: str = None

    def __post_init__(self):
        if self.path is None:
            self.path = os.getenv("DATABASE_PATH", "data.db")


@dataclass
class AuthConfig:
    """JWT authentication configuration."""

    secret_key: str = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    def __post_init__(self):
        if self.secret_key is None:
            self.secret_key = os.getenv("JWT_SECRET_KEY", "change-me-in-production")


@dataclass
class CORSConfig:
    """CORS configuration."""

    dev_mode: bool = None
    allowed_origins: list[str] = None

    def __post_init__(self):
        if self.dev_mode is None:
            self.dev_mode = os.getenv("DEV_MODE", "true").lower() == "true"
        if self.allowed_origins is None:
            origins = os.getenv("ALLOWED_ORIGINS", "")
            self.allowed_origins = [o.strip() for o in origins.split(",") if o.strip()]
