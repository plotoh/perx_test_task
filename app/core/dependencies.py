"""внедрение зависимостей — фабрики для fastapi."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, get_db_session
from app.core.database.repositories.sqlalchemy import SQLAlchemyRepository
from app.core.redis import get_redis_client
from app.services_example.user import UserService
from app.repositories_example.user import UserRepository
from app.models_example.user import User


# сессия бд - посчитал что лучше убрать ее из зависимостей в database
# async def get_session() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         yield session


# фабрика репозитория для любой модели - не работает корректно, для упрощения написал get_user_repository
def get_repository(model):
    def _get_repo(session: AsyncSession = Depends(get_db_session)) -> SQLAlchemyRepository:
        return SQLAlchemyRepository(session, model)

    return _get_repo


# клиент редиса
async def get_redis():
    client = await get_redis_client()
    return client


async def get_user_repository(
        session: AsyncSession = Depends(get_db_session)
) -> UserRepository:
    return UserRepository(session, User)


async def get_user_service(
        repo: UserRepository = Depends(get_user_repository),
        redis=Depends(get_redis),
) -> UserService:
    return UserService(repo, redis)
