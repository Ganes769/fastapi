from .database import Base
from sqlalchemy import Column,Integer,String
class Blog(Base):
    __tablename__="blogs"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    body=Column(String)
class User(Base):
    __tablename__="all_user"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)