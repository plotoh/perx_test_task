"""lifespan вынесен из main"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine, Base
from app.core.redis import get_redis_client, close_redis_client
from app.core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(debug=settings.DEBUG)
    logger.info("запускаемся...")

    # проверка подключение бд
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("база данных ок")
    except Exception as e:
        logger.error(f"база не отвечает: {e}")

    # проверка редис
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
        logger.info("redis ок")
    except Exception as e:
        logger.error(f"redis не отвечает: {e}")

    try:
        # Создаст все таблицы, которые есть в Base.metadata
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("таблицы успешно созданы (или уже существуют)")
    except Exception as e:
        logger.error(f"ошибка при создании таблиц: {e}")

    yield
    # стоп
    logger.info("завершаем работу...")
    await engine.dispose()
    await close_redis_client()
    logger.info("соединения закрыты")