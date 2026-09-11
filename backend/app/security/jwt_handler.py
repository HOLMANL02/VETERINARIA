"""
Emisión y verificación de JWT.
Usa las variables ya definidas en config.py: JWT_SECRET_KEY, JWT_ALGORITHM,
JWT_EXPIRE_MINUTES (access token) y JWT_REFRESH_EXPIRE_DAYS (refresh token).
"""
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt, JWTError

from app.core.config import settings


def _create_token(data: dict[str, Any], expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(usuario_id: int, rol: str) -> str:
    return _create_token(
        {"sub": str(usuario_id), "rol": rol},
        timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
        "access",
    )


def create_refresh_token(usuario_id: int) -> str:
    return _create_token(
        {"sub": str(usuario_id)},
        timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS),
        "refresh",
    )


def decode_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
