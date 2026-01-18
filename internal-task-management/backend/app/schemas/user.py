# app/schemas/user.py
from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    email: str
    role: str

class UserCreate(UserBase):
    password: str  # plain text for now

class UserRead(UserBase):
    id: UUID

    class Config:
        # orm_mode = True
        from_attributes = True

