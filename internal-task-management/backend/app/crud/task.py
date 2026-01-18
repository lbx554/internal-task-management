# app/crud/task.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.crud import task as crud_task
from app.schemas.task import Task, TaskCreate
from app.db.session import SessionLocal

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Task)
def create_task_endpoint(task_in: TaskCreate, db: Session = Depends(get_db)):
    return crud_task.create_task(db, task_in)

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    db_task = crud_task.get_task(db, str(task_id))
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
