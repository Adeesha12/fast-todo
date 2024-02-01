from typing import Annotated
from fastapi import APIRouter, Body, Depends
from passlib.hash import pbkdf2_sha512
from passlib.context import CryptContext

from solution.channel.fastapi.todo_list_manager.controllers.jwt.jwt_handler import sign_jwt
from solution.channel.fastapi.todo_list_manager.schema import UserLoginSchema, UserSchema
from solution.sp.rdb import models
from solution.sp.rdb.db_connection import SessionLocal, get_db

db_dependancy = Annotated[SessionLocal, Depends(get_db)]

user_router = APIRouter(
    prefix="/v1/users",
    tags=["users"]
)

@user_router.post("/user_reg/")
async def user_signup(db:db_dependancy, user:UserSchema = Body(default=None)):
    if check_user_exits(user,db):
        return{
            "error" : "email already exits"
        }
    else:
        return register(user, db)
        

def register(data, db):
    db_user = models.User(**data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return sign_jwt(data.email)

@user_router.post("/user_log/")
async def user_login(db:db_dependancy, user:UserLoginSchema = Body()):
    if check_user(user,db):
        return sign_jwt(user.email)
    else:
        return {
            "error" : "invalid login details !"
        }
        

pwd_context = CryptContext(schemes=['pbkdf2_sha512','md5_crypt'],deprecated=['md5_crypt'])

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def check_user(data: UserLoginSchema,db:db_dependancy):
    user = db.query(models.User).filter(models.User.email==data.email).first()
    return verify_password(data.password,user.password.hash)

def check_user_exits(data:UserSchema,db:db_dependancy):
    if db.query(models.User).filter(models.User.email==data.email).first():
        return True
    