"""fastapi app"""

from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.core.middlewares import LoggingMiddleware
from app.core.exceptions.handlers import (
    app_exception_handler,
    database_exception_handler,
    cache_exception_handler,
)
from app.core.exceptions import AppException, DatabaseException, CacheException

from app.api_example.users import router as users_router


def create_app() -> FastAPI:
    """инициализация приложения"""
    app = FastAPI(
        title="Test Service",
        version="0.1.0",
        lifespan=lifespan,
    )

    # мидлвари
    app.add_middleware(LoggingMiddleware)

    # ручки
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(DatabaseException, database_exception_handler)
    app.add_exception_handler(CacheException, cache_exception_handler)

    # роутеры
    app.include_router(users_router, prefix="/api/v1/users", tags=["users"])

    return app


app = create_app()
