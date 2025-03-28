from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks: List[Task] = []
task_id_counter = 1

@app.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/tasks/", response_class=HTMLResponse)
async def create_task(request: Request, title: str = Form(...), description: Optional[str] = Form(None)):
    global task_id_counter
    new_task = Task(id=task_id_counter, title=title, description=description)
    task_id_counter += 1
    tasks.append(new_task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

