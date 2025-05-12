from  fastapi import FastAPI,Depends
from .schema import Blog
from . import schema,models
from .database import engine,SessionLocaL
from sqlalchemy.orm import Session
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

@app.get("/blog")
def get_all_blog(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs