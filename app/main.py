from hashlib import new
from operator import mod
from pydoc import ModuleScanner
from threading import stack_size
from turtle import pos, title
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from random import randrange ##to temporary generate IDs for the posts

from psycopg2.extras import RealDictCursor

from app.routers.vote import vote  ##To rerturn the column name with the query (by default it is not available)
from . import models,schemas, utils
from .database import engine, SessionLocal
from . import models
from .utils import *
from.routers import post, user, auth,vote
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

# Dependency
#Creates connection with the database and then close the connection once the
#Operation has been performed

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Creating an instance of fastapi  ##
app = FastAPI()

#Define the list of domains through which we want to receive the request
origins = ['*']

#middleware is a function that runs before every request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    


## Until we setup a connection with DB, all the request will get stored in a local variable
# my_posts = [{"title":"title of post 1", "content":"content of post 1","id":"id of post 1"},
# {"title": "favourite food", "content": " I like pizza", "id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

## Path operation
@app.get("/")
async def root():
    return {"message": "welcome to my api"}



