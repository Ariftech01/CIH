import os
from pydantic import BaseModel
from .env import BASE_DIR


class Settings(BaseModel):
    """
    Enterprise Settings Manager for CIH runtime configuration.
    Values come from environment variables and .env files only.
    """

    PROJECT_NAME: str = "Agentic AI for Safety Monitoring with Construction Risk Analytics"
    VERSION: str = "1.0.0"
    APP_ENV: str = os.getenv("APP_ENV", os.getenv("ENVIRONMENT", "development"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", os.getenv("APP_ENV", "development"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t") if os.getenv("APP_ENV") == "production" else True

    # Database Configuration. The runtime should always read DATABASE_URL.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", os.getenv("SUPABASE_KEY", ""))
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SSL_MODE: str = os.getenv("SSL_MODE", "require" if os.getenv("APP_ENV") == "production" else "prefer")

    # Connection Pool Settings
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "1800"))

    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "prod-cih-secret-key-32-chars-long-secure!")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "prod-cih-jwt-secret-32-chars-long-secure!")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = str(BASE_DIR / "logs")

    # AI Services Configuration
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3.2")


settings = Settings()
