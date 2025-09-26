from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_current_user
from app.schemas.todo_schema import (
    TodoCreate, 
    TodoUpdate, 
    TodoResponse, 
    TodoListResponse,
    TodoStatus
)
from app.services.todo_service import TodoService

router = APIRouter()

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Create a new todo item for the current user.
    """
    return TodoService.create_todo(db=db, todo=todo, user_id=current_user["user_id"])

@router.get("/", response_model=TodoListResponse)
def list_todos(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, gt=0, le=100, description="Number of items to return"),
    status: Optional[TodoStatus] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Retrieve todos for the current user with optional status filtering.
    """
    result = TodoService.get_user_todos(
        db=db,
        user_id=current_user["user_id"],
        skip=skip,
        limit=limit,
        status=status
    )
    return result

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Get a specific todo by ID.
    """
    todo = TodoService.get_todo_by_id(
        db=db, 
        todo_id=todo_id, 
        user_id=current_user["user_id"]
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Update a todo item.
    """
    todo = TodoService.update_todo(
        db=db,
        todo_id=todo_id,
        todo_update=todo_update,
        user_id=current_user["user_id"]
    )
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> None:
    """
    Delete a todo item.
    """
    success = TodoService.delete_todo(
        db=db,
        todo_id=todo_id,
        user_id=current_user["user_id"]
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return None