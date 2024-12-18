import json

from redis.asyncio.client import Redis

from application.services.users.schema import UserSchema, UsersSchema


class UsersCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_users(self) -> UsersSchema:
        async with self.redis as redis:
            tasks_json = await redis.lrange("tasks", 0, -1)
            return UsersSchema(users=[UserSchema.model_validate(json.loads(task)) for task in tasks_json])

    async def set_users_by_search(self, search: str, limit: int, offset: int, users_cache: UsersSchema) -> None:
        async with self.redis as redis:
            key = f"search:{search}:limit:{limit}:offset:{offset}"
            pipeline = redis.pipeline()
            for user in users_cache.users:
                pipeline.rpush(key, user.json())
            pipeline.expire(key, 20)
            await pipeline.execute()

    async def get_users_by_query_params(self, search: str, limit: int, offset: int) -> UsersSchema:
        async with self.redis as redis:
            key = f"search:{search}:limit:{limit}:offset:{offset}"
            tasks_json = await redis.lrange(key, 0, -1)
            return UsersSchema(users=[UserSchema.model_validate(json.loads(task)) for task in tasks_json])

    async def set_users(self, users: UsersSchema) -> None:
        users_json = [task.model_dump_json() for task in users.users]
        async with self.redis as redis:
            for task_json in users_json:
                await redis.pipeline().lpush("tasks", task_json).expire("tasks", 20).execute()
