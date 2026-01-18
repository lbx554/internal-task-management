from datetime import datetime, timedelta, timezone
from jose import jwt

SECURITY_KEY = "CHANGE_ME"  # In production, use a secure key from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)
    return encoded_jwt