from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from solution.channel.fastapi.todo_list_manager.controllers.jwt.jwt_handler import decode_jwt
from solution.channel.fastapi.todo_list_manager.controllers.jwt.jwt_bearer import JWTBearer
from solution.channel.fastapi.todo_list_manager.schema import Task
from solution.sp.rdb.db_connection import get_db
from solution.sp.rdb import models



task_router = APIRouter(
    prefix = "/v1/todos",
    tags = ["todos"]
)

db_dependancy = Annotated[Session, Depends(get_db)]


async def get_current_user_id(db:db_dependancy, token: str = Depends(JWTBearer()) ) -> dict:
    # skipping verify since its already verified in JWTBearer
    payload = decode_jwt(token)
    email = payload.get("user_id")
    user = db.query(models.User).filter(models.User.email==email).first()
    user_id = user.UserID
    return user_id


@task_router.post("/task",dependencies=[Depends(JWTBearer())])
def create_task(todo:Task ,db:db_dependancy, current_user_id: int = Depends(get_current_user_id)):
    
    task_data = todo.model_dump()
    task_data["UserID"] = current_user_id
    
    task = models.Task(**task_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    db.close()
    return task

@task_router.get("/task",dependencies=[Depends(JWTBearer())])
def get_tasks(db:db_dependancy, current_user_id: int = Depends(get_current_user_id)):
    results = db.query(models.Task).filter(models.Task.UserID==current_user_id).all()
    return results

@task_router.put("/task/{task_id}", dependencies=[Depends(JWTBearer())])
def update_tasks(task_id: int, task: Task , db:db_dependancy, current_user_id: int = Depends(get_current_user_id)):
    db_task = db.query(models.Task).filter(models.Task.TaskID == task_id, models.Task.UserID==current_user_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for field, value in task.model_dump().items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@task_router.delete("/task/{task_id}", dependencies=[Depends(JWTBearer())])
def delete_tasks(task_id: int, task: Task , db:db_dependancy, current_user_id: int = Depends(get_current_user_id)):
    db_task = db.query(models.Task).filter(models.Task.TaskID == task_id, models.Task.UserID==current_user_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_task)
    db.commit()
    return db_task