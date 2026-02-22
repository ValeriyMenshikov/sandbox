from datetime import datetime
from typing import Optional

from sqlalchemy import text
from sqlalchemy.engine import Result

from application.data_access.pg.base_repositoty import BaseRepository
from application.logger import LOGGER


class AdminRepository(BaseRepository):
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
        try:
            # Экранируем имя пользователя и пароль для безопасного использования в SQL
            safe_username = username.replace("'", "''")
            safe_password = password.replace("'", "''")

            # Форматируем дату истечения в формате PostgreSQL
            expiration_date_str = expiration_date.strftime("%Y-%m-%d %H:%M:%S")

            # Создаем пользователя
            await self.execute(
                text(
                    f"CREATE USER \"{safe_username}\" WITH PASSWORD '{safe_password}' VALID UNTIL '{expiration_date_str}'"
                )
            )

            # Назначаем права только на чтение для всех таблиц в схеме public
            await self.execute(text(f'GRANT USAGE ON SCHEMA public TO "{safe_username}"'))

            await self.execute(text(f'GRANT SELECT ON ALL TABLES IN SCHEMA public TO "{safe_username}"'))

            # Устанавливаем права по умолчанию для будущих таблиц
            await self.execute(
                text(f'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "{safe_username}"')
            )

            LOGGER.info(f"Successfully created read-only user '{username}' with expiration date: {expiration_date_str}")
        except Exception as e:
            LOGGER.error(f"Error creating read-only user: {e}")
            # Если произошла ошибка, пытаемся удалить пользователя, если он был создан
            try:
                await self.execute(text(f'DROP USER IF EXISTS "{safe_username}"'))
            except Exception as drop_error:
                LOGGER.error(f"Failed to drop user after error: {drop_error}")
            raise Exception(f"Failed to create read-only user: {str(e)}")

    async def revoke_user_access(self, username: str) -> None:
        """
        Отзывает доступ у пользователя PostgreSQL.

        Args:
            username: Имя пользователя PostgreSQL

        Raises:
            Exception: Если не удалось отозвать доступ
        """
        try:
            # Экранируем имя пользователя для безопасного использования в SQL
            safe_username = username.replace("'", "''")

            # Отзываем все права
            await self.execute(text(f'REVOKE ALL PRIVILEGES ON SCHEMA public FROM "{safe_username}"'))

            await self.execute(text(f'REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM "{safe_username}"'))

            # Устанавливаем дату истечения на текущую дату, чтобы немедленно отозвать доступ
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await self.execute(text(f"ALTER USER \"{safe_username}\" VALID UNTIL '{current_time}'"))

            LOGGER.info(f"Successfully revoked access for user '{username}'")
        except Exception as e:
            LOGGER.error(f"Error revoking user access: {e}")
            raise Exception(f"Failed to revoke user access: {str(e)}")

    async def check_user_exists(self, username: str) -> bool:
        """
        Проверяет, существует ли пользователь PostgreSQL.

        Args:
            username: Имя пользователя PostgreSQL

        Returns:
            bool: True, если пользователь существует, иначе False
        """
        try:
            # Экранируем имя пользователя для безопасного использования в SQL
            safe_username = username.replace("'", "''")

            result: Result = await self.execute(text(f"SELECT 1 FROM pg_roles WHERE rolname = '{safe_username}'"))

            return result.scalar() is not None
        except Exception as e:
            LOGGER.error(f"Error checking if user exists: {e}")
            return False

    async def get_user_expiration_date(self, username: str) -> Optional[datetime]:
        """
        Получает дату истечения прав пользователя PostgreSQL.

        Args:
            username: Имя пользователя PostgreSQL

        Returns:
            Optional[datetime]: Дата истечения прав пользователя или None, если пользователь не существует
            или у него нет срока действия
        """
        try:
            # Экранируем имя пользователя для безопасного использования в SQL
            safe_username = username.replace("'", "''")

            result: Result = await self.execute(
                text(f"SELECT rolvaliduntil FROM pg_roles WHERE rolname = '{safe_username}'")
            )

            expiration_date = result.scalar()

            if expiration_date is not None:
                return expiration_date

            return None
        except Exception as e:
            LOGGER.error(f"Error getting user expiration date: {e}")
            return None

    async def extend_user_access(self, username: str, new_expiration_date: datetime) -> None:
        """
        Продлевает срок действия прав пользователя PostgreSQL.

        Args:
            username: Имя пользователя PostgreSQL
            new_expiration_date: Новая дата истечения прав пользователя

        Raises:
            Exception: Если не удалось продлить срок действия прав
        """
        try:
            # Экранируем имя пользователя для безопасного использования в SQL
            safe_username = username.replace("'", "''")

            # Форматируем дату истечения в формате PostgreSQL
            expiration_date_str = new_expiration_date.strftime("%Y-%m-%d %H:%M:%S")

            # Продлеваем срок действия прав
            await self.execute(text(f"ALTER USER \"{safe_username}\" VALID UNTIL '{expiration_date_str}'"))

            LOGGER.info(f"Successfully extended access for user '{username}' until {expiration_date_str}")
        except Exception as e:
            LOGGER.error(f"Error extending user access: {e}")
            raise Exception(f"Failed to extend user access: {str(e)}")

    async def upsert_forum_moderator(
        self,
        forum_moderator_id: str,
        forum_id: str,
        user_id: str,
    ) -> None:
        try:
            await self.execute(
                text(
                    'INSERT INTO public."ForumModerators" ("ForumModeratorId", "ForumId", "UserId")\n'
                    'VALUES (:forum_moderator_id, :forum_id, :user_id)\n'
                    'ON CONFLICT ("ForumModeratorId") DO UPDATE\n'
                    'SET "ForumId" = EXCLUDED."ForumId", "UserId" = EXCLUDED."UserId"'
                ).bindparams(
                    forum_moderator_id=forum_moderator_id,
                    forum_id=forum_id,
                    user_id=user_id,
                )
            )
        except Exception as e:
            LOGGER.error(f"Error upserting forum moderator: {e}")
            raise Exception(f"Failed to upsert forum moderator: {str(e)}")

    async def get_forum_moderator(self, forum_moderator_id: str) -> Optional[dict[str, str]]:
        try:
            result: Result = await self.execute(
                text(
                    'SELECT "ForumModeratorId", "ForumId", "UserId"\n'
                    'FROM public."ForumModerators"\n'
                    'WHERE "ForumModeratorId" = :forum_moderator_id'
                ).bindparams(
                    forum_moderator_id=forum_moderator_id,
                ),
                autocommit=False,
            )
            row = result.mappings().one_or_none()
            if row is None:
                return None
            return {
                "forum_moderator_id": str(row["ForumModeratorId"]),
                "forum_id": str(row["ForumId"]),
                "user_id": str(row["UserId"]),
            }
        except Exception as e:
            LOGGER.error(f"Error getting forum moderator: {e}")
            raise Exception(f"Failed to get forum moderator: {str(e)}")
