from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum

Base = declarative_base()

class TodoStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TodoStatus), default=TodoStatus.PENDING, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    owner = relationship("User", back_populates="todos")
