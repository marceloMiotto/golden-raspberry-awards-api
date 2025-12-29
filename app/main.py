from fastapi import FastAPI
from app.core.logging import configure_logging
from app.api.routes import router
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.awards_db import load_csv
from app.services.awards_service import get_awards_intervals

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    db: Session = SessionLocal()
    try:
        load_csv("data/movielist.csv", db)
        yield
    finally:        
        db.close()


@app.get("/producers/awards-intervals")
def get_producers_awards_interval():
    return get_awards_intervals()



