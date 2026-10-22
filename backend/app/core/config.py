"""
Application settings loaded from environment variables via Pydantic Settings.

Usage:
    from app.core.config import settings
    print(settings.environment)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application metadata
    app_name: str = "Pune Water Network AI"
    app_version: str = "0.1.0"
    environment: str = "development"

    # Security
    secret_key: str = "change-me-in-production"

    # CORS — comma-separated list of allowed origins
    allowed_origins: str = "http://localhost:5173"

    # Database (not yet used in the foundation; connection implemented in Stage 2)
    database_url: str = "postgresql+asyncpg://pguser:changeme@localhost:5432/pune_water_network"

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse comma-separated origins string into a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


# Module-level singleton — import and use `settings` throughout the application
settings = Settings()
