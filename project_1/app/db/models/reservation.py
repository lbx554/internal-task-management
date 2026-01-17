# db/models/reservation.py

import enum
from sqlalchemy import UUID, Column, Enum, ForeignKey, Integer, DateTime, Index
from datetime import datetime, timezone
from app.db.base import Base

# Use python's enum, not sqlalchemy's Enum
class ReservationStatus(enum.Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    OVERRIDDEN = "overridden"
    
# Reservation model
class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="RESTRICT"), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id', ondelete="RESTRICT"), nullable=False)
    event_id = Column(UUID, index=True, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.ACTIVE)

    # start_time < end_time
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default = datetime.now(timezone.utc),
        nullable=False
    )

    def __repr__(self):
        return f"<Reservation(user_id={self.user_id}, resource_id={self.resource_id}, event_id={self.event_id}, status={self.status})>"
    
# Index to optimize queries for overlapping reservations on the same resource
Index(
    'ix_reservation_resource_time', 
    Reservation.resource_id, 
    Reservation.start_time, 
    Reservation.end_time,
    postgresql_where=Reservation.status == ReservationStatus.ACTIVE,
)