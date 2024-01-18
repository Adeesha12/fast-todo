from pydantic import BaseModel, EmailStr ,Field
from datetime import date

# class BookItem(BaseModel):
#     title: str = Field(default=None)
#     Author: str = Field(default=None)
#     Publication_Date: date  = Field(default=None)
#     ISBN: int = Field(default=None)
#     Cover_Image: str = Field(default=None)
    
    
class UserSchema(BaseModel):
    username: str = Field(default=None)
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
