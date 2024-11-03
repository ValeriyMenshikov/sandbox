import json

from redis import asyncio as Redis  # noqa: N812

from application.clients.http.dm_api_account.models.api_models import UserDetailsEnvelope


class AccountCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_login(self, token: str) -> str | None:
        async with self.redis as redis:
            login = await redis.get(f"login:{token}")
            return login.decode("utf-8") if login else None

    async def set_login(self, token: str, login: str) -> None:
        async with self.redis as redis:
            await redis.setex(f"login:{token}", 20, login)

    async def get_account_info(self, login: str) -> UserDetailsEnvelope:
        async with self.redis as redis:
            key = f"user:{login}:details"
            details = await redis.get(key)
            return UserDetailsEnvelope.model_validate(json.loads(details))

    async def set_account_info(self, user_details: UserDetailsEnvelope) -> None:
        async with self.redis as redis:
            login = user_details.resource.login
            key = f"user:{login}:details"
            await redis.pipeline().set(key, user_details.json()).expire(key, 20).execute()

    async def set_delete_account_token(self, token: str, delete_token: bytes) -> None:
        async with self.redis as redis:
            await redis.setex(f"delete_account:{token}", 360, delete_token)

    async def get_delete_account_token(self, token: str) -> str | None:
        async with self.redis as redis:
            delete_token = await redis.get(f"delete_account:{token}")
            return delete_token.decode("utf-8") if delete_token else None
