from sqlalchemy import delete, select

from application.clients.db.pg.dm.orm_models import User
from application.data_access.pg.base_repositoty import BaseRepository


class AccountRepository(BaseRepository):
    async def get_user(self, login) -> User:
        user: User = (await self.execute(select(User).where(User.Login == login))).scalar_one_or_none()
        return user

    async def delete_account(self, login) -> None:
        await self.execute(delete(User).where(User.Login == login))
