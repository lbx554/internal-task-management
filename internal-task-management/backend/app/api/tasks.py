from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead  # Minimal schemas
from app.core.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        assigned_to=task.assigned_to
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Task).all()
    return db.query(Task).filter(Task.assigned_to == current_user.id).all()