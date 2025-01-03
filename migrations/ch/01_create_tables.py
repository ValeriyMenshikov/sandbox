import asyncio

from httpx import AsyncClient, Limits

from application.data_access.ch.access import ChClient
from application.settings import Settings


async def main() -> None:
    settings = Settings()
    async with ChClient(
        AsyncClient(limits=Limits(max_keepalive_connections=10)),
        url=settings.ch_url,
        user=settings.CH_USER,
        password=settings.CH_PASSWORD,
        database="default",
    ) as client:
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {settings.CH_DB}"
        await client.execute(create_db_query)

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {settings.CH_DB}.user_registration_events (
            id UUID,
            request_data Nullable(String),
            status_code UInt16,
            error_message Nullable(String),
            event_time DateTime
        ) ENGINE = MergeTree()
        ORDER BY event_time;
        """

        await client.execute(create_table_query)

        response = await client.fetch(query=f"SELECT * FROM {settings.CH_DB}.user_registration_events")
        for i in response:
            print(i["id"], i["request_data"], i["status_code"], i["error_message"], i["event_time"])


asyncio.run(main())
