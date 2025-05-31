from  fastapi import FastAPI,Depends,Response,status,HTTPException
from .schema import Blog
from typing import List
from . import schema,models
from .database import engine,SessionLocaL,get_db
from sqlalchemy.orm import Session # type: ignore
from .hash import Hash
from .routers import blog
app=FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
@app.post("/user",response_model=schema.ShowUser)
def create_user(request:schema.User,db:Session=Depends(get_db)):
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcryptpwd(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@app.get("/user/{id}",response_model=schema.ShowUser)
def getUser(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f"user not found with the {id}")
    return user