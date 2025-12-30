
from sqlalchemy.orm import Session
from app.db.models import Movie
import csv


def load_csv(file_path: str, db: Session) -> None:
        
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")  

        rows_to_insert = []
        for row in reader:
            rows_to_insert.append(
                Movie(
                    year=int(row["year"]),
                    title=row.get("title"),
                    studios=row.get("studios"),
                    producers=row.get("producers"),
                    winner=row.get("winner"),                    
                )
            )

    if rows_to_insert:
        db.bulk_save_objects(rows_to_insert)
        db.commit()

