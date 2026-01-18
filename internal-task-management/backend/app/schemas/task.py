# app/schemas/task.py
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    assigned_to: Optional[UUID] = None

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: UUID

    class Config:
        orm_mode = True

