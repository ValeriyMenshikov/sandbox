from sqlalchemy import select

from application.clients.db.pg.dm.orm_models import User
from application.data_access.pg.base_repositoty import BaseRepository
from application.services.users.schema import UserSchema, UsersSchema


class UsersRepository(BaseRepository):
    async def get_users(self, limit: int, offset: int) -> UsersSchema:
        query = (
            select(
                User.Login,
                User.Name,
                User.Location,
                User.Icq,
                User.Skype,
                User.Info,
            )
            .limit(limit)
            .offset(offset)
        )
        users: list[User] = (await self.execute(query)).fetchall()
        users_list = []
        for user in users:
            serialized_user = UserSchema(
                login=user.Login,
                name=user.Name,
                location=user.Location,
                icq=user.Icq,
                skype=user.Skype,
                info=user.Info,
            )
            users_list.append(serialized_user)

        return UsersSchema(users=users_list)

    async def search_users(self, query: str, limit: int, offset: int) -> UsersSchema:
        query = (
            select(
                User.Login,
                User.Name,
                User.Location,
                User.Icq,
                User.Skype,
                User.Info,
            )
            .where(User.Login.like(f"%{query}%"))
            .limit(limit)
            .offset(offset)
        )
        users: list[User] = (await self.execute(query)).fetchall()
        users_list = []
        for user in users:
            serialized_user = UserSchema(
                login=user.Login,
                name=user.Name,
                location=user.Location,
                icq=user.Icq,
                skype=user.Skype,
                info=user.Info,
            )
            users_list.append(serialized_user)

        return UsersSchema(users=users_list)
