
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks: List[Task] = []
task_id_counter = 1

@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    global task_id_counter
    task.id = task_id_counter
    task_id_counter += 1
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
async def get_all_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            updated_task.id = task_id 
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

