import email
from typing import Optional
from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

from app.database import Base

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True




## For users
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
     orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

#This will inherit everything from PostBase
class PostCreate(PostBase):
    pass

##Creating class for the Response
#Define the data to be sent back to FE

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    ## This will help convert SQL Alchemy model into pydantic model
    #only required for response models
    class Config:
     orm_mode = True

class PostOut(PostBase):
    Post: Post
    votes:int

    class Config:
     orm_mode = True

#In the schema, no need to define the user id as it can be obtained from the token
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
