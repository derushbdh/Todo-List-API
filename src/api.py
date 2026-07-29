import os
import jwt
from fastapi import FastAPI, HTTPException, Header, Depends
from sqlalchemy.orm import Session

from src.schemas import TaskCreate, TaskUpdateDesc, TaskUpdatePrior, TaskUpdateStatus, UserCreate
from src import crud
from src.models import Task
from src.db import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)
SECRET_KEY = "my_super_secret_key_which_is_now_at_least_32_bytes_long"
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(authorization: str = Header(None)) -> int:
    if authorization is None:
        raise HTTPException(status_code = 401, detail = "Not authorized")
    
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms = ["HS256"])
        return payload.get("user_id")
    except (jwt.InvalidTokenError, IndexError):
        raise HTTPException(status_code = 401, detail = "Invalid token")


@app.post("/tasks")
def create_task(
    data: TaskCreate, 
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
    ):
    new_task = Task(description = data.description, priority = data.priority)
    crud.add_task(db, new_task, user_id)

    return {"message": "Successfully created", "task_id": new_task.id}

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int, 
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
    ):
    success = crud.delete_task(db, task_id, user_id)

    if not success:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return {"message": f"Task {task_id} successfully deleted"}

@app.put("/tasks/{task_id}/description")
def update_desc(
    task_id: int, 
    updated_desc: TaskUpdateDesc,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
    ):
    success = crud.update_description(db, user_id, task_id, updated_desc.description)

    if not success:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return {"message": f"Task {task_id} description successfully updated"}

@app.put("/tasks/{task_id}/priority")
def update_prior(
    task_id: int, 
    updated_prior: TaskUpdatePrior,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
    ):
    success = crud.update_priority(db, user_id, task_id, updated_prior.priority)

    if not success:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return {"message": f"Task {task_id} priority successfully updated"}

@app.put("/tasks/{task_id}/status")
def update_status(
    task_id: int, 
    updated_status: TaskUpdateStatus,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
    ):
    success = crud.update_status(db, user_id, task_id, updated_status.status)

    if not success:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return {"message": f"Task {task_id} status successfully updated"}

@app.get("/tasks")
def get_tasks(
    status: str = "", 
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
    ):   
    return crud.list_tasks(db, user_id=user_id, status=status)


@app.post("/register")
def create_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
    ):
    success = crud.register_user(db, user_data.username, user_data.password)

    if not success:
        raise HTTPException(status_code = 400, detail = "This username occupied") 
    return {"message": f"Successfull registration"}

@app.post("/login")
def login_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
    ):
    user_id = crud.authenticate_user(db, user_data.username, user_data.password)

    if user_id is None:
        raise HTTPException(status_code = 401, detail = "Incorrect login or password")
    
    payload = {"user_id": user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm = "HS256")

    return {"access_token": token, "token_type": "bearer"}