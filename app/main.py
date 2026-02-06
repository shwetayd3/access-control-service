from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging

def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(
        title="Access Control Service",
        version="0.1.0",
        debug=settings.DEBUG
    )

    app.include_router(health_router, prefix="/health", tags=["health"])
    return app

app = create_app()
