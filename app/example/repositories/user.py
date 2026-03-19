"""репозиторий пользователя"""
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.database.repositories.sqlalchemy import SQLAlchemyRepository
from app.example.models.user import User


class UserRepository(SQLAlchemyRepository[User]):

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

