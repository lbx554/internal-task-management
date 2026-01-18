import uuid
from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from datetime import datetime, timezone

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum("未着手", "進行中", "完了", name="task_status"), default="未着手", nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))