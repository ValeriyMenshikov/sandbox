from dataclasses import dataclass

from application.services.users.repository.users_cache import UsersCache
from application.services.users.repository.users_repository import UsersRepository
from application.services.users.schema import UsersSchema


@dataclass
class UsersService:
    users_repository: UsersRepository
    users_cache: UsersCache

    async def get_users(self, limit: int, offset: int) -> UsersSchema:
        users = await self.users_cache.get_users()
        if not users.users:
            users = await self.users_repository.get_users(limit=limit, offset=offset)
            await self.users_cache.set_users(users)
        return users

    async def search_users(self, search: str, limit: int, offset: int) -> UsersSchema:
        users = await self.users_cache.get_users_by_query_params(search=search, limit=limit, offset=offset)
        if not users.users:
            users = await self.users_repository.search_users(search=search, limit=limit, offset=offset)
            await self.users_cache.set_users_by_search(search=search, limit=limit, offset=offset, users_cache=users)
        return users
