from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class TodoStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TodoStatus] = None

class TodoResponse(TodoBase):
    id: int
    status: TodoStatus
    user_id: int
    created_at: str

    class Config:
        from_attributes = True

class TodoListResponse(BaseModel):
    todos: List[TodoResponse]
    total: int
    skip: int
    limit: int
