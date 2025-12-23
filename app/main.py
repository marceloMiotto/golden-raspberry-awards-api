from fastapi import FastAPI
from app.core.logging import configure_logging

def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Golden Raspberry Awards Service",
        version="1.0.0",
        description="RESTful API that provides access to nominees and winners of the Worst Picture category at the Golden Raspberry Awards.",
    )

    return app

app = create_app()