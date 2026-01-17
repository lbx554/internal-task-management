from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import SessionLocal
from app.db.models.reservation import Reservation, ReservationStatus
from app.db.models.resource import Resource
from app.db.models.user import User
from typing import List
from uuid import uuid4
from pydantic import BaseModel, ConfigDict
from datetime import datetime

router = APIRouter()

# APIRouter -> FastAPI's way to modularize endpoints
# SessionLocal -> DB session for queries
# Reservation, Resource, User -> Our SQLAlchemy models
# uuid4 -> generate unique event_id for each reservation
# BaseModel -> define request/response schemas (date validation)
# and_ -> SQLAlchemy helper for combining multiple conditions in queries

# What the client sends when creating a reservation
class ReservationCreate(BaseModel):
    user_id: int    # Note: user_id will come from auth context later
    resource_id: int
    start_time: datetime
    end_time: datetime

# what we return (includes generated event_id and status)
class ReservationResponse(BaseModel):
    event_id: str
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime
    status: str

    """# Allows FASTAPI/Pydantic to read directly from SQLAlchemy model instances
    class Config:
        orm_mode = True"""
    model_config = ConfigDict(from_attributes=True)

# Every request that interact with db gets a session via this dependency
# This ensures sessions are created and closed properly, even on errors
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Enforces "no overlapping reservations" rule
def check_overlap(db: Session, resource_id: int, start_time: datetime, end_time: datetime):
    overlapping = db.query(Reservation).filter(
        Reservation.resource_id == resource_id,
        Reservation.status == ReservationStatus.ACTIVE,
        # Check for time overlap
        and_(
            Reservation.start_time < end_time,
            Reservation.end_time > start_time
        )
    ).first()
    return overlapping is not None

@router.post("/", response_model=ReservationResponse)
def create_reservation(res: ReservationCreate, db: Session = Depends(get_db)):
    # Check resource exists
    resource = db.query(Resource).filter(Resource.id == res.resource_id, Resource.is_active == True).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Check user exists
    user = db.query(User).filter(User.id == res.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check for overlap
    overlapping = check_overlap(db, res.resource_id, res.start_time, res.end_time)
    if overlapping:
        raise HTTPException(status_code=409, detail="Time slot overlaps with existing reservation")

    # Create reservation
    reservation = Reservation(
        user_id=res.user_id,
        resource_id=res.resource_id,
        start_time=res.start_time,
        end_time=res.end_time,
        event_id=str(uuid4()),  # unique identifier
        status=ReservationStatus.ACTIVE
    )
    try:
        db.add(reservation)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create reservation")
    
    db.refresh(reservation)
    return reservation
