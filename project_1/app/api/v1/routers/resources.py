from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.db.models.resource import Resource
from pydantic import BaseModel, ConfigDict

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ResourceCreate(BaseModel):
    name: str
    description: str | None = None

class ResourceResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(res: ResourceCreate, db: Session = Depends(get_db)):
    resource = Resource(
        name=res.name,
        description=res.description,
        is_active=True
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource

@router.get("/", response_model=List[ResourceResponse])
def list_resources(db: Session = Depends(get_db), active_only: bool = True):
    resources = db.query(Resource).filter(Resource.is_active == True).all()
    return resources

@router.patch("/{resource_id}/deactivate", response_model=ResourceResponse)
def deactivate_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource.is_active = False
    db.commit()
    db.refresh(resource)
    return {"message": "Resource deactivated", "resource": resource}

@router.patch("/{resource_id}/activate", response_model=ResourceResponse)
def activate_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource.is_active = True
    db.commit()
    db.refresh(resource)
    return {"message": "Resource activated", "resource": resource}

