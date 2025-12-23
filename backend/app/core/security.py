from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "60"))

MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password is required")

    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise ValueError("Password must be at most 72 characters")

    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    if not password or not hashed:
        return False

    return pwd_context.verify(password, hashed)


def create_access_token(data: dict) -> str:
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is not set")

    if "sub" not in data:
        raise ValueError("Token payload must include 'sub'")

    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_MIN)
    to_encode = {**data, "exp": expire}

    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
