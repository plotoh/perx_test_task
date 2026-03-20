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
    logger.info("запуск")

    # проверка подключений
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Подключение к бд -- ОК")
    except Exception as e:
        logger.critical(f"Подключение к бд не удалось: {e}")
        raise RuntimeError("Подключение к бд не удалось") from e
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
        logger.info("Подключение к редису -- ОК")
    except Exception as e:
        logger.critical(f"Подключение к редису не удалось: {e}")
        raise RuntimeError("Подключение к редису не удалось") from e

    # создание таблиц. изначально хотел сделать алембик, но думаю для тестового уместно и через base
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы успешно созданы / подтверждены")
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        raise RuntimeError("Ошибка при создании таблиц") from e

    yield

    # стоп
    logger.info("Инициирую закрытие подклюеий")
    await engine.dispose()
    await close_redis_client()
    logger.info("Подключения закрыты")
