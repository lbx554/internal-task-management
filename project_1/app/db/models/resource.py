# db/models/resource.py

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.base import Base


class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default = datetime.now(timezone.utc),
        nullable=False
    )


    def __repr__(self):
        return f"<Resource(name={self.name}, description={self.description}, is_active={self.is_active})>"