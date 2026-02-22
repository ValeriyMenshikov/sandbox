from datetime import datetime, timedelta

import uuid

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status

from application.dependency.dependency import get_admin_service
from application.logger import LOGGER
from application.services.admin.schema import (
    CreateReadOnlyUserRequest,
    CreateReadOnlyUserResponse,
    ExtendUserAccessRequest,
    ExtendUserAccessResponse,
    GetForumModeratorResponse,
    RevokeUserAccessResponse,
    UpsertForumModeratorRequest,
    UpsertForumModeratorResponse,
    UserExpirationResponse,
)
from application.services.admin.service import AdminService
from application.utils import service_error_handler

app = FastAPI(title="Admin API")
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/postgres/users/readonly",
    response_model=CreateReadOnlyUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_readonly_user(
    request: CreateReadOnlyUserRequest,
    admin_service: AdminService = Depends(get_admin_service),  # noqa: B008
) -> CreateReadOnlyUserResponse:
    """
    Создает пользователя PostgreSQL с правами только на чтение и сроком действия.
    """
    async with service_error_handler():
        # Создаем дату истечения прав без информации о часовом поясе
        expiration_date = datetime.now() + timedelta(days=request.expiration_days)

        await admin_service.create_readonly_user(
            username=request.username,
            password=request.password,
            expiration_date=expiration_date,
        )

        LOGGER.info(f"Created read-only PostgreSQL user: {request.username} with expiration date: {expiration_date}")

        return CreateReadOnlyUserResponse(
            username=request.username,
            expiration_date=expiration_date,
            message=f"Пользователь {request.username} успешно создан с правами только на чтение до {expiration_date}",
        )


@router.delete(
    "/postgres/users/{username}",
    response_model=RevokeUserAccessResponse,
    status_code=status.HTTP_200_OK,
)
async def revoke_user_access(
    username: str,
    admin_service: AdminService = Depends(get_admin_service),  # noqa: B008
) -> RevokeUserAccessResponse:
    """
    Отзывает доступ у пользователя PostgreSQL.
    """
    async with service_error_handler():
        await admin_service.revoke_user_access(username=username)

        return RevokeUserAccessResponse(
            username=username,
            message=f"Доступ пользователя {username} успешно отозван",
        )


@router.get(
    "/postgres/users/{username}/expiration",
    response_model=UserExpirationResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_expiration_date(
    username: str,
    admin_service: AdminService = Depends(get_admin_service),  # noqa: B008
) -> UserExpirationResponse:
    """
    Получает дату истечения прав пользователя PostgreSQL.
    """
    async with service_error_handler():
        expiration_date = await admin_service.get_user_expiration_date(username=username)

        # Убедимся, что обе даты имеют одинаковый тип (без информации о часовом поясе)
        now = datetime.now()
        if expiration_date.tzinfo is not None:
            # Если expiration_date содержит информацию о часовом поясе, удалим ее
            expiration_date = expiration_date.replace(tzinfo=None)

        days_left = (expiration_date - now).days

        return UserExpirationResponse(
            username=username,
            expiration_date=expiration_date,
            days_left=days_left,
        )


@router.patch(
    "/postgres/users/{username}/extend",
    response_model=ExtendUserAccessResponse,
    status_code=status.HTTP_200_OK,
)
async def extend_user_access(
    username: str,
    request: ExtendUserAccessRequest,
    admin_service: AdminService = Depends(get_admin_service),  # noqa: B008
) -> ExtendUserAccessResponse:
    """
    Продлевает срок действия прав пользователя PostgreSQL.
    """
    async with service_error_handler():
        new_expiration_date = await admin_service.extend_user_access(
            username=username,
            days_to_extend=request.days_to_extend,
        )

        # Убедимся, что дата не содержит информацию о часовом поясе
        if new_expiration_date.tzinfo is not None:
            new_expiration_date = new_expiration_date.replace(tzinfo=None)

        LOGGER.info(
            f"Extended access for PostgreSQL user: {username} for {request.days_to_extend} days. "
            f"New expiration date: {new_expiration_date}"
        )

        return ExtendUserAccessResponse(
            username=username,
            new_expiration_date=new_expiration_date,
            days_extended=request.days_to_extend,
            message=f"Доступ пользователя {username} успешно продлен на {request.days_to_extend} дней. "
            f"Новая дата истечения прав: {new_expiration_date}",
        )


@router.post(
    "/forum/moderators",
    response_model=UpsertForumModeratorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upsert_forum_moderator(
    request: UpsertForumModeratorRequest,
    admin_service: AdminService = Depends(get_admin_service),  # noqa: B008
) -> UpsertForumModeratorResponse:
    async with service_error_handler():
        await admin_service.upsert_forum_moderator(
            forum_moderator_id=request.forum_moderator_id,
            forum_id=request.forum_id,
            user_id=request.user_id,
        )

        return UpsertForumModeratorResponse(
            forum_moderator_id=request.forum_moderator_id,
            forum_id=request.forum_id,
            user_id=request.user_id,
            message="Forum moderator upserted",
        )


@router.get(
    "/forum/moderators/{forum_moderator_id}",
    response_model=GetForumModeratorResponse,
    status_code=status.HTTP_200_OK,
)
async def get_forum_moderator(
    forum_moderator_id: uuid.UUID,
    admin_service: AdminService = Depends(get_admin_service),  # noqa: B008
) -> GetForumModeratorResponse:
    async with service_error_handler():
        data = await admin_service.get_forum_moderator(forum_moderator_id=forum_moderator_id)
        if data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum moderator not found")

        return GetForumModeratorResponse(
            forum_moderator_id=uuid.UUID(data["forum_moderator_id"]),
            forum_id=uuid.UUID(data["forum_id"]),
            user_id=uuid.UUID(data["user_id"]),
        )


app.include_router(router)
