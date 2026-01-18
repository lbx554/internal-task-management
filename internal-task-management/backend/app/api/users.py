from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserRead  # We'll create minimal schemas
from app.core.security import get_current_user


router = APIRouter(prefix="/users", tags=["users"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Only admins can create users
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        hashed_password=User.hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
