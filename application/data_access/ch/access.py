import orjson
from aiochclient import ChClient
from httpx import AsyncClient, Limits

from application.settings import Settings


async def get_ch_connection() -> ChClient:
    settings = Settings()
    async with ChClient(
        AsyncClient(limits=Limits(max_keepalive_connections=10)),
        url=settings.ch_url,
        user=settings.CH_USER,
        password=settings.CH_PASSWORD,
        database=settings.CH_DB,
        json=orjson,
    ) as client:
        yield client


async def get_ch_client() -> ChClient:
    settings = Settings()
    return ChClient(
        AsyncClient(limits=Limits(max_keepalive_connections=10)),
        url=settings.ch_url,
        user=settings.CH_USER,
        password=settings.CH_PASSWORD,
        database=settings.CH_DB,
        json=orjson,
    )
