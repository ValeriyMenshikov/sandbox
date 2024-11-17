from fastapi import APIRouter, Depends, FastAPI

from application.dependency.dependency import get_users_service
from application.services.users.schema import UsersSchema
from application.services.users.service import UsersService
from application.utils import service_error_handler

app = FastAPI(title="Users API")
router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    path="/users",
    summary="Получить список пользователей",
    description="Метод для получения списка пользователей.",
    response_model_exclude_none=True,
)
async def get_users(
    limit: int = 10,
    offset: int = 0,
    users_service: UsersService = Depends(get_users_service),  # noqa: B008
) -> UsersSchema:
    async with service_error_handler():
        return await users_service.get_users(limit=limit, offset=offset)


@router.get(
    path="/users/search",
    summary="Поиск пользователей",
    description="Метод для поиска пользователей.",
    response_model_exclude_none=True,
)
async def search_users(
    search: str,
    limit: int = 10,
    offset: int = 0,
    users_service: UsersService = Depends(get_users_service),  # noqa: B008
) -> UsersSchema:
    async with service_error_handler():
        return await users_service.search_users(search=search, limit=limit, offset=offset)


app.include_router(router)
