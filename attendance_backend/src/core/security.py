from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import hashlib
import hmac
import base64
import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def _sign(message: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode(), message, hashlib.sha256).digest()
    return _b64encode(sig)

def _json_dumps(obj: Any) -> bytes:
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode()

def _json_loads(data: bytes) -> Any:
    return json.loads(data.decode())

# PUBLIC_INTERFACE
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a minimal JWT-compatible token (HS256) without external dependencies.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    header = {"alg": "HS256", "typ": "JWT"}
    payload = to_encode | {"exp": int(expire.timestamp())}
    header_b64 = _b64encode(_json_dumps(header))
    payload_b64 = _b64encode(_json_dumps(payload))
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = _sign(signing_input, settings.SECRET_KEY)
    return f"{header_b64}.{payload_b64}.{signature}"

def _decode_token(token: str) -> dict:
    try:
        header_b64, payload_b64, signature = token.split(".")
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = _sign(signing_input, settings.SECRET_KEY)
        if not hmac.compare_digest(signature, expected_sig):
            raise ValueError("Invalid token signature")
        payload = _json_loads(_b64decode(payload_b64))
        exp = int(payload.get("exp", 0))
        if int(datetime.now(timezone.utc).timestamp()) > exp:
            raise ValueError("Token expired")
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

# Simple password hashing using sha256 + salt (for demo, replace with bcrypt/argon2 in production)
_SALT = "attendance_salt"

# PUBLIC_INTERFACE
def get_password_hash(password: str) -> str:
    """Hash a password using sha256 + static salt."""
    return hashlib.sha256(f"{_SALT}:{password}".encode()).hexdigest()

# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hash."""
    return hmac.compare_digest(get_password_hash(plain_password), hashed_password)

# PUBLIC_INTERFACE
def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Extract current user id from Bearer token."""
    payload = _decode_token(token)
    return payload.get("sub")
