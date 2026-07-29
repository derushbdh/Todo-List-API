from sqlalchemy import Column, Integer, String
from src.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index = True)
    description = Column(String, nullable=False)
    status = Column(String, default="todo")
    created_at = Column(String)
    updated_at = Column(String, nullable=True)
    priority = Column(String, default="medium")
    user_id = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)