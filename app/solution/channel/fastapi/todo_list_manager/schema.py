from pydantic import BaseModel, EmailStr ,Field
from datetime import date

class Task(BaseModel):
    TaskTitle: str = Field(default=None)
    Description: str = Field(default=None)
    DueDate: date  = Field(default=None)
    IsComplete: bool = Field(default=None)



class UserSchema(BaseModel):
    Username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema ={
            "User_demo" : {
                "name":"Bob",
                "email":"Bob@eaxample.com",
                "password":"123@4"
            }
        }
    


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema ={
            "User_demo" : {
                "email":"Bob@eaxample.com",
                "password":"123@4"
            }
        }
