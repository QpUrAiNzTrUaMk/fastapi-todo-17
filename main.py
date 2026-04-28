import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TODO API for Railway")

class Task(BaseModel):
    id: int
    title: str
    done: bool = False
    client_name: str  # твоё поле (вариант 17)

db: List[Task] = []

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return db

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    if any(t.id == task.id for t in db):
        raise HTTPException(status_code=400, detail="ID already exists")
    db.append(task)
    return task

@app.patch("/tasks/{id}/done", response_model=Task)
async def mark_done(id: int):
    for task in db:
        if task.id == id:
            task.done = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
async def delete_task(id: int):
    global db
    db = [t for t in db if t.id != id]
    return {"message": f"Task {id} deleted"}

@app.get("/info")
async def get_info():
    return {
        "status": os.getenv("APP_STATUS", "development"),
        "platform": "Railway"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)