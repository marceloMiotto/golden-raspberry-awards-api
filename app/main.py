import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.core.logging import configure_logging
from app.api.routes import router
from app.db.session import SessionLocal, engine
from app.db.awards_db import load_csv
from app.db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)    
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        default_csv = Path(__file__).resolve().parent / "data" / "movielist.csv"
        csv_path = os.getenv("CSV_PATH", str(default_csv))
        load_csv(csv_path, db)
        yield
    finally:
        
        db.close()


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Golden Raspberry Awards Service",
        version="1.0.0",
        description="RESTful API that provides access to nominees and winners of the Worst Picture category at the Golden Raspberry Awards.",
        lifespan=lifespan,
    )

    app.include_router(router, prefix="/api")
    return app


app = create_app()
