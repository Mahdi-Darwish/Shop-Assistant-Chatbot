from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    groq_api_key: str
    # Redis is required for the production rate limiter.
    redis_url: str

    # In development the API can be called locally/file://.
    # In production, set FRONTEND_URL to the exact deployed UI origin.
    environment: str = "development"
    frontend_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
