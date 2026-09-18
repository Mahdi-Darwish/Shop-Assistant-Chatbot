from slowapi import Limiter
from fastapi import Request
from slowapi.util import get_remote_address
from app.core.config import settings
from app.core.security import decode_access_token

def rate_limiter_key(request:Request) ->str:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer"):
        token = auth_header.removeprefix("Bearer")
        payload = decode_access_token(token)
        if payload and payload.get("user_id"):
            return f"user:{payload["user_id"]}"
        return f"ip{get_remote_address(request)}"

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.redis_url,
    swallow_errors=False,
    default_limits=["100/minute"],
)
