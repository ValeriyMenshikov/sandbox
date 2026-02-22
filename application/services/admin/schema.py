from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field


class CreateReadOnlyUserRequest(BaseModel):
    """Запрос на создание пользователя PostgreSQL с правами только на чтение."""

    username: str = Field(..., description="Имя пользователя PostgreSQL")
    password: str = Field(..., description="Пароль пользователя PostgreSQL")
    expiration_days: Optional[int] = Field(30, description="Срок действия прав в днях")


class CreateReadOnlyUserResponse(BaseModel):
    """Ответ на запрос создания пользователя PostgreSQL с правами только на чтение."""

    username: str
    expiration_date: datetime
    message: str


class ExtendUserAccessRequest(BaseModel):
    """Запрос на продление доступа пользователя PostgreSQL."""

    days_to_extend: int = Field(..., description="Количество дней, на которое нужно продлить доступ")


class ExtendUserAccessResponse(BaseModel):
    """Ответ на запрос продления доступа пользователя PostgreSQL."""

    username: str
    new_expiration_date: datetime
    days_extended: int
    message: str


class UserExpirationResponse(BaseModel):
    """Ответ на запрос информации о дате истечения прав пользователя PostgreSQL."""

    username: str
    expiration_date: datetime
    days_left: int


class RevokeUserAccessResponse(BaseModel):
    """Ответ на запрос отзыва доступа пользователя PostgreSQL."""

    username: str
    message: str


class UpsertForumModeratorRequest(BaseModel):
    forum_moderator_id: uuid.UUID = Field(..., description="ForumModeratorId")
    forum_id: uuid.UUID = Field(..., description="ForumId")
    user_id: uuid.UUID = Field(..., description="UserId")


class UpsertForumModeratorResponse(BaseModel):
    forum_moderator_id: uuid.UUID
    forum_id: uuid.UUID
    user_id: uuid.UUID
    message: str


class GetForumModeratorResponse(BaseModel):
    forum_moderator_id: uuid.UUID
    forum_id: uuid.UUID
    user_id: uuid.UUID
