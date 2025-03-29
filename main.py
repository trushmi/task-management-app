from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from sqlalchemy.orm import Session
from database import SessionLocal, Task as DBTask  

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class TaskStatus(str, Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Task(BaseModel):
    id: Optional[int] = None 
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.LOW

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(DBTask).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks, "TaskPriority": TaskPriority})

@app.post("/tasks/", response_class=HTMLResponse)
async def create_task(
    request: Request,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    status: TaskStatus = Form(TaskStatus.TODO),
    priority: TaskPriority = Form(TaskPriority.MEDIUM),
    db: Session = Depends(get_db)
):
    db_task = DBTask(title=title, description=description, status=status.value, priority=priority.value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": db.query(DBTask).all(), "TaskPriority": TaskPriority})

@app.post("/tasks/{task_id}/update/", response_class=HTMLResponse)
async def update_task(
    request: Request,
    task_id: int,
    status: TaskStatus = Form(...),
    priority: TaskPriority = Form(...),
    db: Session = Depends(get_db)
):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.status = status.value
    db_task.priority = priority.value
    db.commit()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": db.query(DBTask).all(), "TaskPriority": TaskPriority})