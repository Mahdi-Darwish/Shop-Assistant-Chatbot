import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.config import settings
from app.core.rate_limit import limiter
from app.routes import admin_routes, chat_routes, user_routes,admin_chat_routes

logger = logging.getLogger("uvicorn.error")
app = FastAPI(title="Shop API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your real frontend's domain once deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
@app.on_event("startup")
def check_redis_connection() -> None:
    """Redis is only reachable lazily (on first real request) unless we
    proactively check it here. We deliberately do NOT let a failed check
    stop the app from starting — swallow_errors=True on the limiter means
    the app is fully functional without Redis, just without rate limiting.
    This just gets the problem into your logs immediately on deploy,
    instead of silently discovering it days later."""
    try:
        import redis

        client = redis.from_url(settings.redis_url, socket_connect_timeout=2)
        client.ping()
        logger.info("Rate limiter: connected to Redis at %s", settings.redis_url)
    except Exception as exc:
        logger.warning(
            "Rate limiter: could not reach Redis (%s) — requests will be "
            "served WITHOUT rate limiting until Redis is available "
            "(swallow_errors is enabled, so the app itself is unaffected).",
            exc,
        )
app.include_router(user_routes.router)
app.include_router(admin_routes.router)
app.include_router(admin_chat_routes.router)
app.include_router(chat_routes.router)

# Run with: uvicorn app.server:app --reload