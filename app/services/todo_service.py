from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.database.models import Todo, TodoStatus
from app.schemas.todo_schema import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse

class TodoService:
    @staticmethod
    def create_todo(db: Session, todo: TodoCreate, user_id: int):
        db_todo = Todo(
            title=todo.title,
            description=todo.description,
            user_id=user_id
        )
        
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    
    @staticmethod
    def get_user_todos(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 10,
        status: Optional[TodoStatus] = None
    ):
        query = db.query(Todo).filter(Todo.user_id == user_id)
        
        if status:
            query = query.filter(Todo.status == status)
        
        total = query.count()
        todos = query.offset(skip).limit(limit).all()
        
        return TodoListResponse(
            todos=todos,
            total=total,
            skip=skip,
            limit=limit
        )
    
    @staticmethod
    def get_todo_by_id(db: Session, todo_id: int, user_id: int):
        return db.query(Todo).filter(and_(Todo.id == todo_id, Todo.user_id == user_id)).first()
    
    @staticmethod
    def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate, user_id: int):
        db_todo = db.query(Todo).filter(and_(Todo.id == todo_id, Todo.user_id == user_id)).first()
        
        if not db_todo:
            return None
        
        update_data = todo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        
        db.commit()
        db.refresh(db_todo)
        return db_todo
    
    @staticmethod
    def delete_todo(db: Session, todo_id: int, user_id: int) -> bool:
        db_todo = db.query(Todo).filter(and_(Todo.id == todo_id, Todo.user_id == user_id)).first()
        
        if not db_todo:
            return False
        
        db.delete(db_todo)
        db.commit()
        return True