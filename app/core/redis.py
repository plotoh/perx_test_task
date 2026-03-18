"""клиент для редиса (синглтон)."""

from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings

_redis_pool: ConnectionPool | None = None
_redis_client: Redis | None = None


async def get_redis_client() -> Redis:
    """возвращает один и тот же клиент (пул)."""
    global _redis_pool, _redis_client
    if _redis_client is None:
        _redis_pool = ConnectionPool.from_url(settings.redis_url, decode_responses=True)
        _redis_client = Redis(connection_pool=_redis_pool)
    return _redis_client


async def close_redis_client() -> None:
    """закрываем соединения при остановке."""
    global _redis_pool, _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
    if _redis_pool:
        await _redis_pool.disconnect()
        _redis_pool = None