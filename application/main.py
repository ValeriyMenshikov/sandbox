import asyncio
import contextlib
import platform
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI

from application import APP_MAP
from application.dependency.dependency import (
    get_kafka_producer,
    get_kafka_register_consumer,
    get_kafka_retry_register_consumer,
)
from application.grpc import grpc_server
from application.settings import Settings

if platform.system() == "Linux":
    processors = [
        structlog.processors.JSONRenderer(ensure_ascii=False),
    ]
else:
    processors = [
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False),
    ]

structlog.configure(processors=processors)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    kafka_producer = await get_kafka_producer(settings=Settings())
    kafka_register_consumer = await get_kafka_register_consumer(kafka_producer)
    kafka_retry_register_consumer = await get_kafka_retry_register_consumer(kafka_producer)
    register = asyncio.create_task(kafka_register_consumer.registration_consume())
    retry = asyncio.create_task(kafka_retry_register_consumer.registration_consume())

    interceptors: list = []
    async with (
        grpc_server(app, interceptors),
    ):
        try:
            yield
        finally:
            register.cancel()
            retry.cancel()
            await kafka_producer.disconnect()
            await kafka_register_consumer.close_connection()
            await kafka_retry_register_consumer.close_connection()


main_app = FastAPI(lifespan=lifespan)


for app_name, app in APP_MAP.items():
    main_app.mount(f"/{app_name}", app)
