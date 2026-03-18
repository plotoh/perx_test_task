"""решил все прописать в init, но уместно вынести в файл"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# пул
engine = create_async_engine(
    settings.database_url,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# сессии
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# абстрактная база для моделей
Base = declarative_base()


async def get_db_session() -> AsyncSession:
    """зависимость отдающая сессию"""
    async with AsyncSessionLocal() as session:
        yield session
