from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status



app=FastAPI()

class Task:
    def __init__(self, id: int, title: str, description: str, done: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.done = done


class TaskRequest(BaseModel):
    id: Optional[int] = Field(None, ge=0)
    title: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    done: bool = False

TASKS=[Task(1,"Task 1","Description 1",False),]   


def get_next_task_id():
    return 1 if len(TASKS) == 0 else TASKS[-1].id + 1



@app.post('/tasks/create_task',status_code=status.HTTP_201_CREATED)
async def create_task(task_request: TaskRequest):
    new_task = Task(get_next_task_id(), task_request.title, task_request.description, task_request.done)
    TASKS.append(new_task)
    return new_task



@app.get("/tasks", status_code=status.HTTP_200_OK)
async def read_all_tasks():
    return TASKS



@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def read_task(task_id: int = Path(gt=0)):
    for task in TASKS:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail='Task not found')



@app.put("/update_tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(task_id: int, task_request: TaskRequest):
    for task in TASKS:
        if task.id == task_id:
            if task_request.title is not None:
                task.title = task_request.title
            if task_request.description is not None:
                task.description = task_request.description
            task.done = task_request.done
            return task
    raise HTTPException(status_code=404, detail='Task not found')
    



@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int = Path(gt=0)):
    for i in range(len(TASKS)):
        if TASKS[i].id == task_id:
            TASKS.pop(i)
            return
    raise HTTPException(status_code=404, detail='Task not found')
    

