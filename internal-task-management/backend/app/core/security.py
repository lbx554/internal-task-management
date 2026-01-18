from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from app.db.session import SessionLocal
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
import os


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECURITY_KEY = os.getenv("SECRET_KEY", "CHANGE_ME") # In production, use a secure key from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Authorization: Bearer <JWT_TOKEN>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = verify_access_token(token)
    email = payload.get("sub")
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)