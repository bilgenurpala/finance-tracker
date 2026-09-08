from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import health
from app.core.config import get_settings
from app.db.base import create_engine, create_redis_pool, create_session_factory


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = create_engine()
    app.state.engine = engine
    app.state.session_factory = create_session_factory(engine)
    app.state.redis_pool = create_redis_pool()
    try:
        yield
    finally:
        await app.state.redis_pool.aclose()
        await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    is_production = settings.ENVIRONMENT == "production"
    application = FastAPI(
        title="FinTrack API",
        version="0.1.0",
        lifespan=lifespan,
        docs_url=None if is_production else "/docs",
        redoc_url=None if is_production else "/redoc",
        openapi_url=None if is_production else "/openapi.json",
    )
    application.include_router(health.router)
    return application


app = create_app()
