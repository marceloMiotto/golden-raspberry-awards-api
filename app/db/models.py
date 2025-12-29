from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"

    id=Column(Integer, primary_key=True, index=True)
    year=Column(Integer)
    title=Column(String)
    studios=Column(String)
    producers=Column(String)
    winner=Column(String)  
