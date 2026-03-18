"""ошибки для веба"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

from app.core.exceptions import (
    AppException,
    DatabaseException,
    CacheException,
    NotFoundError,
    ValidationError,
)

logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.error(f"внутренняя ошибка сервера: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "внутренняя ошибка сервера"},
    )


async def database_exception_handler(request: Request, exc: DatabaseException) -> JSONResponse:
    logger.error(f"база данных временно недоступна: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "база данных временно недоступна"},
    )


async def cache_exception_handler(request: Request, exc: CacheException) -> JSONResponse:
    logger.error(f"кэш временно недоступен: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "кэш временно недоступен"},
    )


async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc) or "ресурс не найден"},
    )


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc) or "ошибка валидации"},
    )
