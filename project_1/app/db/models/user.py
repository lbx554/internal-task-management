# db/models/user.py

from datetime import datetime, timezone
import enum
from sqlalchemy import Column, Enum, Integer, String, DateTime
from app.db.base import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False) # unique=true creates
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default = datetime.now(timezone.utc),
        nullable=False
    )

    def __repr__(self):
        return f"<User(email={self.email}, role={self.role})>"
    
    