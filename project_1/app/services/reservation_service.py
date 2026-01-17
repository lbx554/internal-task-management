# services/reservation_service.py 
# -> Handles business logic for reservations
# -> DB sessions are passed in (no direct FastAPI dependency)
# -> keeps routers thin

import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from db.models import Reservation, ReservationStatus

class ReservationService:
    @staticmethod
    def create_reservation(db: Session, user_id: uuid.UUID, resource_id: uuid.UUID, start_time: datetime, end_time: datetime) -> Reservation:
        # Validate times
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")

        # Check for overlapping reservations
        overlapping = db.query(Reservation).filter(
            Reservation.resource_id == resource_id,
            Reservation.status == ReservationStatus.ACTIVE,
            # Check for time overlap
            and_(
                Reservation.start_time < end_time,
                Reservation.end_time > start_time
            )
        ).first()

        if overlapping:
            raise ValueError("Resource is already booked for the requested time slot.")
        
        # Check if user has overlapping reservations
        user_overlapping = db.query(Reservation).filter(
            Reservation.user_id == user_id,
            Reservation.status == ReservationStatus.ACTIVE,
            # Check for time overlap
            and_(
                Reservation.start_time < end_time,
                Reservation.end_time > start_time
            )
        ).first()

        if user_overlapping:
            raise ValueError("User has an overlapping reservation.")
        
        # Generate event_id
        event_id = uuid.uuid4()

        new_reservation = Reservation(
            user_id=user_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            status=ReservationStatus.PENDING,
            event_id=event_id
        )

        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation) # Return fully populated object
        return new_reservation