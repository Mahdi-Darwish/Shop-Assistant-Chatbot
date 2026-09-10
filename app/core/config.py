# What it does: Loads settings (DATABASE_URL, JWT_SECRET, etc.) from your .env file into a typed object, instead of scattering os.getenv() calls everywhere.
# Why this way: pydantic-settings validates on startup — if JWT_SECRET is missing, the app crashes immediately with a clear error instead of failing silently later when someone tries to log in. It also gives you autocomplete/type-checking (settings.jwt_secret instead of a raw string key that could typo).
# Reusable as-is: 100%. Copy this file into any project unchanged — just make sure the .env has matching keys. It's the standard pattern for config management in FastAPI apps      
# from pydantic_settings import BaseSettings
# class Settings(BaseSettings):
#     database_url: str
#     gemini_api_key: str
#     jwt_secret: str
#     jwt_algorithm:str= "HS256"
#     access_token_expire_minutes:int= 60 * 24
#     class Config:
#         env_file = ".env"
# settings = Settings()


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 day
    # gemini_api_key:str
    groq_api_key: str
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()