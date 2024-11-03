from dataclasses import dataclass

from application.services.users.repository.users_repository import UsersRepository
from application.services.users.schema import UsersSchema


@dataclass
class UsersService:
    users_repository: UsersRepository

    async def get_users(self, limit: int, offset: int) -> UsersSchema:
        # TODO: добавить кэш
        return await self.users_repository.get_users(limit=limit, offset=offset)

    async def search_users(self, query: str, limit: int, offset: int) -> UsersSchema:
        # TODO: добавить кэш
        return await self.users_repository.search_users(query=query, limit=limit, offset=offset)
