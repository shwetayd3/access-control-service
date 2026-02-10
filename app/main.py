from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.auth import router as auth_router
from app.api.oauth import router as oauth_router

def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(
        title="Access Control Service",
        version="0.1.0",
        debug=settings.DEBUG
    )

    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(auth_router)
    app.include_router(oauth_router)
    return app

app = create_app()
