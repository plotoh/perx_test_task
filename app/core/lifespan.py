"""lifespan вынесениз main"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from app.core.database import engine, AsyncSessionLocal
from app.core.redis import redis_client
from app.core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    что делать при старте и остановке.
    """
    # стартуем
    setup_logging(debug=app.debug)
    logger.info("запускаемся...")

    # проверка подключение бд
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        logger.info("база данных ок")
    except Exception as e:
        logger.error(f"база не отвечает: {e}")

    # проверка редис
    try:
        await redis_client.ping()
        logger.info("redis ок")
    except Exception as e:
        logger.error(f"redis не отвечает: {e}")

    yield

    # стоп
    logger.info("завершаем работу...")
    await engine.dispose()
    await redis_client.close()
    logger.info("соединения закрыты")