from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from solution.channel.fastapi.todo_list_manager.schema import Task
from solution.sp.rdb import models
from solution.channel.fastapi.todo_list_manager.controllers.jwt.jwt_bearer import JWTBearer
from solution.sp.rdb.db_connection import get_db


task_router = APIRouter(
    prefix = "/v1/todos",
    tags = ["todos"]
)

db_dependancy = Annotated[Session, Depends(get_db)]

@task_router.post("/task",dependencies=[Depends(JWTBearer())])
def create_task(todo:Task ,db:db_dependancy):
    task = models.Task(**todo.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    db.close()
    return task

@task_router.get("/task",dependencies=[Depends(JWTBearer())])
def get_tasks(db:db_dependancy):
    results = db.query(models.Task).all()
    return results

@task_router.put("/task/{task_id}", dependencies=[Depends(JWTBearer())])
def update_tasks(task_id: int, task: Task , db:db_dependancy):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for field, value in task.model_dump().items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@task_router.delete("/task/{task_id}", dependencies=[Depends(JWTBearer())])
def delete_tasks(task_id: int, task: Task , db:db_dependancy):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_task)
    db.commit()
    return db_task