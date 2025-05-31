from  fastapi import FastAPI,Depends,Response,status,HTTPException
from .schema import Blog
from typing import List
from . import schema,models
from .database import engine,SessionLocaL,get_db
from sqlalchemy.orm import Session # type: ignore
from .routers import blog
from .routers import user

app=FastAPI()
models.Base.metadata.create_all(engine)
app.include_router(blog.router)
app.include_router(user.router)
