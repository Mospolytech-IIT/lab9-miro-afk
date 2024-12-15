"Часть 1: Подключение к базе данных и создание таблиц"
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base
engine = create_engine('postgresql://postgres:1234@localhost/Backend')
engine.connect()

Base = declarative_base()

class User(Base):
    "Table users"
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)    
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

class Post(Base):
    "Table posts"
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)    
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(engine)
