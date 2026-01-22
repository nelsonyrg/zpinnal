"""
Configuración central de la aplicación usando Pydantic Settings.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Proyecto
    PROJECT_NAME: str = "Mobile App API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Seguridad
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Base de datos
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/app_db"
    DATABASE_ECHO: bool = False

    # Redis (cache/sesiones)
    REDIS_URL: str = "redis://redis:6379/0"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "capacitor://localhost",
        "ionic://localhost",
    ]


settings = Settings()
