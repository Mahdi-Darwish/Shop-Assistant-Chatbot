from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.database import SessionLocal
from app.models.user_model import User
from app.services.user_services import get_user_by_username

# HTTPBearer (not OAuth2PasswordBearer) — our /login takes a plain JSON
# body, not an OAuth2 form-encoded login. HTTPBearer gives Swagger's
# "Authorize" popup a simple "paste your token" field instead of trying
# to POST username/password/client_id/client_secret as form data to
# /login (which caused the 422 — /login doesn't accept that format).
security_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Decodes the JWT and re-fetches the user from the DB on every request.
    We deliberately re-check the DB rather than trusting the role embedded in
    the token, so a role change (or account deactivation) takes effect
    immediately instead of waiting for the token to expire."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "This account has been deactivated by the admin",
            headers= {"WWW-Authenticate":"Bearer"}
        )
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Use as a dependency on any route that must be restricted to admins,
    e.g. listing all users or all users' phone numbers."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user