# What it does: Four functions — hash a password, verify a password against its hash, create a JWT, decode a JWT.
# Why this way:
# passlib's CryptContext handles bcrypt correctly (salting, cost factor) so you never touch raw hashing logic.
# decode_access_token returns None on failure instead of raising — this keeps the calling code (in dependencies.py) clean, since it just checks "did I get a payload or not" rather than wrapping everything in try/except.
# Token expiry is baked into create_access_token via exp, so an old token is automatically rejected by jwt.decode without you writing manual expiry checks.
# Reusable as-is: Completely. This file has zero knowledge of "users," "shops," or your database — it's pure JWT/hashing utility. Copy it into any project that needs token auth.

from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def decode_access_token(token: str) -> dict | None:
    """Returns the payload if valid, or None if the token is invalid/expired.
    Never raises — callers decide how to respond (usually 401)."""
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None