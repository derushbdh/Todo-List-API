from typing import Any
from sqlalchemy.orm import Session
from src.models import Task, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def add_task(db: Session, task: Task, user_id: int) -> None:
    task.user_id = user_id
    db.add(task)
    db.commit()

    db.refresh(task)

def delete_task(db: Session, task_id: int, user_id: int) -> bool: 
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False

def update_description(db: Session, user_id: int, task_id: int, new_desc: str) -> bool:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        task.description = new_desc
        db.commit()
        return True
    return False

def update_priority(db: Session, user_id: int, task_id: int, new_prior: str) -> bool:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        task.priority = new_prior
        db.commit()
        return True
    return False

def update_status(db: Session, user_id: int, task_id: int, new_status: str) -> bool:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        task.status = new_status
        db.commit()
        return True
    return False

def list_tasks(db: Session, user_id: int, status: str = "") -> list[dict[str, Any]]:
    if not status:
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
    else:
        tasks = db.query(Task).filter(Task.user_id == user_id, Task.status == status).all()
    
    tasks_list = []
    for t in tasks:
        tasks_list.append({
            "id": t.id,
            "description": t.description,
            "status": t.status,
            "created": t.created_at,
            "updated": t.updated_at,
            "priority": t.priority
        })
    return tasks_list


def register_user(db: Session, username: str, password: str) -> bool:
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return False
    
    hashed_password = pwd_context.hash(password)

    new_user = User(username = username, password_hash = hashed_password)

    db.add(new_user)
    db.commit()

    return True

def authenticate_user(db: Session, username: str, password: str) -> int | None:
    existing_user = db.query(User).filter(User.username == username).first()
    if not existing_user or not pwd_context.verify(password, existing_user.password_hash):
        return None
    return existing_user.id