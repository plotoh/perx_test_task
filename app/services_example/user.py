"""бизнес-логика юзера"""
from app.models_example.user import User
from app.repositories_example.user import UserRepository
from redis.asyncio import Redis
import json

from app.schemas.user import UserResponse


class UserService:
    """регистрация и получение пользователя с кэшированием."""

    def __init__(self, repo: UserRepository, cache: Redis):
        self.repo = repo
        self.cache = cache

    async def register_user(self, email: str, name: str) -> User:
        """проверяем юзера + добавляем в кэш"""
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValueError(f"пользователь с email {email} уже есть")

        user = await self.repo.create(email=email, name=name)

        await self.cache.set(
            f"user:{user.id}",
            json.dumps({"id": user.id, "email": user.email, "name": user.name}),
            ex=3600,
        )
        return user

    async def get_user(self, user_id: int) -> UserResponse | None:
        """беремюзера из кэша потом из бд"""
        cached = await self.cache.get(f"user:{user_id}")
        if cached:
            data = json.loads(cached)
            return UserResponse(**data)  # создаём схему из словаря

        user = await self.repo.get(user_id)
        if user:
            # сохраняем в кэш (можно хранить уже как словарь)
            await self.cache.set(
                f"user:{user_id}",
                json.dumps({"id": user.id, "email": user.email, "name": user.name}),
                ex=3600,
            )
            return UserResponse.from_orm(user)
        return None
