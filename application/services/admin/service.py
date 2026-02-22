import dataclasses
from datetime import datetime, timedelta

import uuid
from typing import Optional

from application.logger import LOGGER
from application.services.admin.repository.admin_repository import AdminRepository


@dataclasses.dataclass
class AdminService:
    admin_repository: AdminRepository

    async def create_readonly_user(
        self,
        username: str,
        password: str,
        expiration_date: datetime,
    ) -> None:
        """
        Создает пользователя PostgreSQL с правами только на чтение и сроком действия.

        Args:
            username: Имя пользователя PostgreSQL
            password: Пароль пользователя PostgreSQL
            expiration_date: Дата истечения прав пользователя

        Raises:
            Exception: Если не удалось создать пользователя или назначить права
        """
        # Проверяем, существует ли пользователь
        user_exists = await self.admin_repository.check_user_exists(username)
        if user_exists:
            LOGGER.warning(f"User '{username}' already exists. Updating permissions and expiration date.")
            # Сначала отзываем все права
            await self.admin_repository.revoke_user_access(username)

        # Создаем пользователя или обновляем его права
        await self.admin_repository.create_readonly_user(
            username=username,
            password=password,
            expiration_date=expiration_date,
        )

        LOGGER.info(f"Successfully created/updated read-only user '{username}' with expiration date: {expiration_date}")

    async def revoke_user_access(self, username: str) -> None:
        """
        Отзывает доступ у пользователя PostgreSQL.

        Args:
            username: Имя пользователя PostgreSQL

        Raises:
            Exception: Если не удалось отозвать доступ
        """
        user_exists = await self.admin_repository.check_user_exists(username)
        if not user_exists:
            LOGGER.warning(f"User '{username}' does not exist. Cannot revoke access.")
            return

        await self.admin_repository.revoke_user_access(username)
        LOGGER.info(f"Successfully revoked access for user '{username}'")

    async def get_user_expiration_date(self, username: str) -> datetime:
        """
        Получает дату истечения прав пользователя PostgreSQL.

        Args:
            username: Имя пользователя PostgreSQL

        Returns:
            datetime: Дата истечения прав пользователя

        Raises:
            Exception: Если пользователь не существует или у него нет срока действия
        """
        expiration_date = await self.admin_repository.get_user_expiration_date(username)
        if expiration_date is None:
            raise Exception(f"User '{username}' does not exist or has no expiration date")

        return expiration_date

    async def extend_user_access(self, username: str, days_to_extend: int) -> datetime:
        """
        Продлевает срок действия прав пользователя PostgreSQL.

        Args:
            username: Имя пользователя PostgreSQL
            days_to_extend: Количество дней, на которое нужно продлить доступ

        Returns:
            datetime: Новая дата истечения прав пользователя

        Raises:
            Exception: Если пользователь не существует или не удалось продлить доступ
        """
        # Проверяем, существует ли пользователь
        user_exists = await self.admin_repository.check_user_exists(username)
        if not user_exists:
            raise Exception(f"User '{username}' does not exist")

        # Получаем текущую дату истечения прав
        current_expiration = await self.admin_repository.get_user_expiration_date(username)

        # Если текущая дата истечения прав не установлена, используем текущую дату
        if current_expiration is None:
            current_expiration = datetime.now()

        # Рассчитываем новую дату истечения прав
        new_expiration_date = current_expiration + timedelta(days=days_to_extend)

        # Продлеваем доступ
        await self.admin_repository.extend_user_access(username, new_expiration_date)

        LOGGER.info(f"Successfully extended access for user '{username}' until {new_expiration_date}")

        return new_expiration_date

    async def upsert_forum_moderator(
        self,
        forum_moderator_id: uuid.UUID,
        forum_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        await self.admin_repository.upsert_forum_moderator(
            forum_moderator_id=str(forum_moderator_id),
            forum_id=str(forum_id),
            user_id=str(user_id),
        )

    async def get_forum_moderator(self, forum_moderator_id: uuid.UUID) -> Optional[dict[str, str]]:
        return await self.admin_repository.get_forum_moderator(
            forum_moderator_id=str(forum_moderator_id),
        )
