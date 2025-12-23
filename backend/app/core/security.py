from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", 60))

MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise ValueError("Password must be at most 72 characters")
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict):
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is not set")

    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_MIN)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
