"""абстрактный репозиторий интерфейсов для крудов"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any

ModelType = TypeVar("ModelType")


class BaseRepository(ABC, Generic[ModelType]):
    @abstractmethod
    async def get(self, id: Any) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def get_multi(
            self, *, skip: int = 0, limit: int = 100, **filters
    ) -> List[ModelType]:
        """пагинация и фильтры"""
        pass

    @abstractmethod
    async def create(self, **kwargs) -> ModelType:
        pass

    @abstractmethod
    async def update(self, id: Any, **kwargs) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def delete(self, id: Any) -> bool:
        pass
