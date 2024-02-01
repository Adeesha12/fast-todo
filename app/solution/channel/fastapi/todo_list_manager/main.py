import uvicorn
from fastapi import FastAPI

from solution.channel.fastapi.todo_list_manager.routers.auth import user_router
from solution.channel.fastapi.todo_list_manager.routers.todos import task_router
from solution.sp.rdb.db_connection import engine, Base

Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(user_router)
app.include_router(task_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4)