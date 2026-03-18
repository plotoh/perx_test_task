"""внедрение зависимостей — фабрики для fastapi."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session, AsyncSessionLocal
from app.core.database.repositories.sqlalchemy import SQLAlchemyRepository
from app.core.redis import get_redis_client


# сессия бд
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# фабрика репозитория для любой модели
def get_repository(model):
    def _get_repo(session: AsyncSession = Depends(get_session)) -> SQLAlchemyRepository:
        return SQLAlchemyRepository(session, model)

    return _get_repo


# клиент редиса
async def get_redis():
    client = await get_redis_client()
    return client

