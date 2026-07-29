from pydantic import BaseModel

class TaskCreate(BaseModel):
    description: str
    priority: str = "medium"

class TaskUpdateDesc(BaseModel):
    description: str

class TaskUpdatePrior(BaseModel):
    priority: str

class TaskUpdateStatus(BaseModel):
    status: str


class UserCreate(BaseModel):
    username: str
    password: str