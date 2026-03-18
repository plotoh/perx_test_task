"""ручки для работы с пользователями"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.services_example.user import UserService
from app.core.dependencies import get_user_service
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """создаем нового пользователя"""
    try:
        user = await service.register_user(user_data.email, user_data.name)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """получаем пользователя по id."""
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="пользователь не найден")
    return UserResponse.from_orm(user)