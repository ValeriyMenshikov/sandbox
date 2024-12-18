from sqlalchemy import delete, select, update

from application.clients.db.pg.dm.orm_models import User
from application.data_access.pg.base_repositoty import BaseRepository
from application.services.account.schema import UserSchema


class AccountRepository(BaseRepository):
    async def get_user(self, login: str) -> User:
        user = (await self.execute(select(User).where(User.Login == login))).scalar_one_or_none()
        if user is None:
            raise ValueError("User not found")
        return user

    async def delete_account(self, login: str) -> None:
        await self.execute(delete(User).where(User.Login == login))

    async def update_user(self, user_login: str, user: UserSchema) -> None:
        new_user_data = user.model_dump(by_alias=True)
        await self.execute(update(User).where(User.Login == user_login).values(**new_user_data))
