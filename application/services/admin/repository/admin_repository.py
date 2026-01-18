from datetime import datetime
import re
from typing import Optional

from sqlalchemy import text
from sqlalchemy.engine import Result

from application.data_access.pg.base_repositoty import BaseRepository
from application.logger import LOGGER


class AdminRepository(BaseRepository):
    _USERNAME_RE = re.compile(r"^[a-zA-Z0-9_][a-zA-Z0-9_\-]{0,62}$")

    @classmethod
    def _validate_username(cls, username: str) -> None:
        if not cls._USERNAME_RE.fullmatch(username):
            raise ValueError(
                "Invalid username. Allowed: letters/digits/_/-, length <= 63, must start with letter/digit/_"
            )

    @staticmethod
    def _quote_ident(identifier: str) -> str:
        return '"' + identifier.replace('"', '""') + '"'

    async def _ensure_readonly_role(self) -> None:
        await self.execute(
            text(
                """
                DO $$
                BEGIN
                  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'readonly_role') THEN
                    CREATE ROLE readonly_role;
                  END IF;

                  EXECUTE format('GRANT CONNECT ON DATABASE %I TO readonly_role', current_database());

                  EXECUTE 'GRANT USAGE ON SCHEMA public TO readonly_role';
                  EXECUTE 'GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_role';
                  EXECUTE 'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO readonly_role';

                  EXECUTE 'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_role';
                  EXECUTE 'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO readonly_role';
                END $$;
                """
            )
        )

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
            self._validate_username(username)
            quoted_username = self._quote_ident(username)

            # Форматируем дату истечения в формате PostgreSQL
            expiration_date_str = expiration_date.strftime("%Y-%m-%d %H:%M:%S")

            await self._ensure_readonly_role()

            # Создаем пользователя
            await self.execute(
                text(
                    f"CREATE USER {quoted_username} WITH PASSWORD :password VALID UNTIL :valid_until"
                )
                .bindparams(password=password, valid_until=expiration_date_str)
            )

            await self.execute(text(f"GRANT readonly_role TO {quoted_username}"))
            await self.execute(text(f"ALTER ROLE {quoted_username} CONNECTION LIMIT 3"))

            LOGGER.info(f"Successfully created read-only user '{username}' with expiration date: {expiration_date_str}")
        except Exception as e:
            LOGGER.error(f"Error creating read-only user: {e}")
            # Если произошла ошибка, пытаемся удалить пользователя, если он был создан
            try:
                if 'quoted_username' in locals():
                    await self.execute(text(f"DROP USER IF EXISTS {quoted_username}"))
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
            self._validate_username(username)
            quoted_username = self._quote_ident(username)

            await self.execute(text(f"REVOKE readonly_role FROM {quoted_username}"))

            # Устанавливаем дату истечения на текущую дату, чтобы немедленно отозвать доступ
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await self.execute(text(f"ALTER USER {quoted_username} VALID UNTIL :valid_until").bindparams(valid_until=current_time))

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
            self._validate_username(username)
            result: Result = await self.execute(text("SELECT 1 FROM pg_roles WHERE rolname = :username").bindparams(username=username))

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
            self._validate_username(username)
            result: Result = await self.execute(text("SELECT rolvaliduntil FROM pg_roles WHERE rolname = :username").bindparams(username=username))

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
            self._validate_username(username)
            quoted_username = self._quote_ident(username)

            # Форматируем дату истечения в формате PostgreSQL
            expiration_date_str = new_expiration_date.strftime("%Y-%m-%d %H:%M:%S")

            # Продлеваем срок действия прав
            await self.execute(text(f"ALTER USER {quoted_username} VALID UNTIL :valid_until").bindparams(valid_until=expiration_date_str))

            LOGGER.info(f"Successfully extended access for user '{username}' until {expiration_date_str}")
        except Exception as e:
            LOGGER.error(f"Error extending user access: {e}")
            raise Exception(f"Failed to extend user access: {str(e)}")
