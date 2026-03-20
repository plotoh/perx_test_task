"""ручки для работы с пользователями"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.example.services.user import UserService
from app.core.dependencies import get_user_service
from app.example.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreate,
        service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.register_user(user_data.email, user_data.name)
    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: int,
        service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.get_user(user_id)  # в сервисе пробрасывает ошибки
    return UserResponse.model_validate(user)
