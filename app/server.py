import logging

import redis
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.rate_limit import limiter
from app.database import engine
from app.routes import admin_chat_routes, admin_routes, chat_routes, user_routes

logger = logging.getLogger("uvicorn.error")


app = FastAPI(title="Shop API")


# The browser only needs Authorization headers; the API does not use
# cookie-based authentication, so credentials are intentionally disabled.
if settings.environment.lower() == "production":
    if not settings.frontend_url:
        raise RuntimeError("FRONTEND_URL must be set when ENVIRONMENT=production")
    allowed_origins = [settings.frontend_url.rstrip("/")]
else:
    # Keeps local Docker + a locally opened static UI working during development.
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
        "null",  # local file:// pages
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.on_event("startup")
def check_redis_connection() -> None:
    """Fail startup if Redis is unavailable.

    Redis is part of the production security setup because SlowAPI uses it
    for rate-limit storage. Silently disabling rate limiting is not acceptable
    in production.
    """
    client = redis.from_url(
        settings.redis_url,
        socket_connect_timeout=2,
        socket_timeout=2,
    )
    try:
        client.ping()
        logger.info("Rate limiter: connected to Redis")
    except Exception as exc:
        logger.error("Rate limiter: Redis is unavailable: %s", exc)
        raise RuntimeError("Redis is required but unavailable") from exc
    finally:
        client.close()


@app.get("/health", tags=["system"])
def health_check():
    """Health check for Render and production monitoring."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        client = redis.from_url(
            settings.redis_url,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        try:
            client.ping()
        finally:
            client.close()

        return {"status": "ok"}
    except Exception:
        logger.exception("Health check failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service dependencies are unavailable",
        )


app.include_router(user_routes.router)
app.include_router(admin_routes.router)
app.include_router(admin_chat_routes.router)
app.include_router(chat_routes.router)
