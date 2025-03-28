from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

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
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM  # Default priority

tasks: List[Task] = []
task_id_counter = 1

@app.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks, "TaskPriority": TaskPriority})

@app.post("/tasks/", response_class=HTMLResponse)
async def create_task(
    request: Request,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    status: TaskStatus = Form(TaskStatus.TODO),
    priority: TaskPriority = Form(TaskPriority.MEDIUM)
):
    global task_id_counter
    new_task = Task(id=task_id_counter, title=title, description=description, status=status, priority=priority)
    task_id_counter += 1
    tasks.append(new_task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks, "TaskPriority": TaskPriority})
