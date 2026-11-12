from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Task(BaseModel):
    id: UUID | None = None
    title: str
    description: str | None = None
    completed: bool = False


tasks = []


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task


@app.get("/tasks/", response_model=list[Task])
def read_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.model_copy(
                update=task_update.model_dump(exclude_unset=True)
            )
            tasks[idx] = updated_task
            return updated_task
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(idx)
    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
