"""бизнес-логика юзера"""
from app.example.models.user import User
from app.example.repositories.user import UserRepository
from redis.asyncio import Redis
import json

from app.example.schemas.user import UserResponse


class UserService:
    """регистрация и получение пользователя с кэшированием."""

    def __init__(self, repo: UserRepository, cache: Redis):
        self.repo = repo
        self.cache = cache

    async def register_user(self, email: str, name: str) -> User:
        """проверяем юзера + добавляем в кэш"""
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValidationError(f"пользователь с email {email} уже есть")

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
            return UserResponse(**data)

        user = await self.repo.get(user_id)
        if not user:
            raise NotFoundError(f"пользователь с id {user_id} не найден")

        user_data = {"id": user.id, "email": user.email, "name": user.name}
        await self.cache.set(f"user:{user_id}", json.dumps(user_data), ex=3600)
        return UserResponse.model_validate(user)
