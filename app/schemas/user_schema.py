# What it does: Defines the shape of data coming in (UserSignup, UserLogin) and going out (UserOut, Token), with validation rules attached.

# Why this way:

# UserSignup validates password strength, phone format, and password-confirmation match before your route code even runs — bad requests get rejected automatically with a clear 422 error.
# UserOut deliberately excludes hashed_password. This is the actual mechanism that prevents a password hash from ever leaking in an API response — even if you're lazy later and do return user somewhere, FastAPI serializes through UserOut and drops the field.

# Reusable as-is: The structure (separate input/output schemas, validators) is reusable everywhere. The content — phone regex, password rules, exact fields — is specific to this app and you'd adjust it per project (e.g. an app with email instead of phone).
import re
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
PHONE_PATTERN = re.compile(r"^[0-9+ ]{7,15}$")
class UserSignup(BaseModel):
    username: str
    password: str
    confirm_password: str
    phone: str
    @field_validator("username")
    @classmethod
    def username_length(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v
    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Za-z]", v) or not re.search(r"[0-9]", v):
            raise ValueError("Password must contain both letters and numbers")
        return v
    @field_validator("phone")
    @classmethod
    def phone_format(cls, v: str) -> str:
        v = v.strip()
        if not PHONE_PATTERN.match(v):
            raise ValueError("Invalid phone number")
        return v
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
class UserLogin(BaseModel):
    username: str
    password: str
class UserOut(BaseModel):
    """Safe to return to a client — never includes hashed_password."""
    id: int
    username: str
    phone: str
    role: str
    model_config = ConfigDict(from_attributes=True)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"