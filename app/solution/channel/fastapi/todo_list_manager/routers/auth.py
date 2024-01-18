from typing import Annotated
from fastapi import APIRouter, Depends

from solution.sp.rdb import models
from solution.sp.rdb.db_connection import SessionLocal, get_db

db_dependancy = Annotated[SessionLocal, Depends(get_db)]

user_router = APIRouter(
    prefix="/v1/users",
    tags=["users"]
)

@user_router.post("/user_reg/")
async def register(data,db:db_dependancy):
    return register(data, db)

def register(data, db):
    db_user = models.User(**data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user