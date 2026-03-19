"""внедрение зависимостей"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, get_db_session
from app.core.database.repositories.sqlalchemy import SQLAlchemyRepository
from app.core.redis import get_redis_client
from app.example.services import UserService
from app.example.repositories import UserRepository
from app.example.models import User


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
