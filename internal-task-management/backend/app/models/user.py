import uuid
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from datetime import datetime, timezone
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum("admin", "user", name="role_enum"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

# hash a password
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    # verify a password
    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)