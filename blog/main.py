from  fastapi import FastAPI,Depends,Response,status,HTTPException
from .schema import Blog
from typing import List
from . import schema,models
from .database import engine,SessionLocaL
from sqlalchemy.orm import Session # type: ignore
from .hash import Hash
app=FastAPI()
models.Base.metadata.create_all(engine)
def get_db():
    db=SessionLocaL()
    try:
        yield db
    finally:
        db.close()
@app.post("/blog")
def create_blog(blog:schema.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=blog.title,body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog",response_model=List[schema.ShowBlog])
def get_all_blog(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs
@app.get("/blog/{id}",status_code=200,response_model=schema.ShowBlog)
def get__blog(id,response:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return{"message":f"Blog with the id {id} not available"}
    return blog

@app.delete("/blog/{id}",status_code=200)
def desroy(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=404,detail=f"blog with {id} is not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"blog deleted"}

@app.put("/blog/{id}",status_code=202)
def updtae(id,request:schema.Blog,db:Session=Depends(get_db)):
    print(request)
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=404,detail=f"blog with {id} is not found")
    blog.update({"title":request.title,"body":request.body})
    print(request)
    db.commit()
    return {"blog updtated  "}
    
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