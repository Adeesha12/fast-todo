import uvicorn
from fastapi import FastAPI

from solution.channel.fastapi.todo_list_manager.routers import auth

app = FastAPI()
app.include_router(auth)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4)