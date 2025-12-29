
from app.db.session import get_db
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import csv


Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"

    id=Column(Integer, primary_key=True, index=True)
    year=Column(Integer)
    title=Column(String)
    studios=Column(String)
    producers=Column(String)
    winner=Column(String)  


def load_csv(file_path: str, db: Session) -> None:
        
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)  

        rows_to_insert = []
        for row in reader:
            rows_to_insert.append(
                Movie(
                    year=int(row.get("winner")),
                    title=row.get("title"),
                    studios=row.get("studios"),
                    producers=row.get("producers"),
                    winner=row.get("winner"),                    
                )
            )

    if rows_to_insert:
        db.bulk_save_objects(rows_to_insert)
        db.commit()

