# db/models/audit_log.py

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, index=True)
    actor_user_id = Column(Integer, ForeignKey('users.id'))
    target_reservation_id = Column(Integer, ForeignKey('reservation.id'))
    action = Column(String)
    reason = Column(String)
    created_at = Column(String)

    def __repr__(self):
        return f"<AuditLog(actor_user_id={self.actor_user_id})>"