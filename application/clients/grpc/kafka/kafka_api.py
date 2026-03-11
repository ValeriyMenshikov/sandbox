from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncIterator

import grpc
from aiokafka import AIOKafkaConsumer
from google.protobuf import empty_pb2

from application.clients.grpc.kafka import kafka_pb2, kafka_pb2_grpc
from application.logger import LOGGER
from application.settings import Settings


@dataclass
class KafkaStreamService(kafka_pb2_grpc.KafkaStreamServiceServicer):
    settings: Settings

    async def Subscribe(  # noqa: N802
        self,
        request: empty_pb2.Empty,
        context: grpc.aio.ServicerContext,
    ) -> AsyncIterator[kafka_pb2.KafkaMessage]:
        metadata = {item.key: item.value for item in context.invocation_metadata()}
        topic = metadata.get("topic")
        offset = metadata.get("offset", "latest").lower()

        if not topic:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "metadata 'topic' is required")

        if offset not in {"latest", "earliest"}:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "metadata 'offset' must be latest or earliest")

        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.settings.KAFKA_URL,
            auto_offset_reset=offset,
            enable_auto_commit=False,
        )

        try:
            await consumer.start()
            async for message in consumer:
                if not context.is_active():
                    break
                yield kafka_pb2.KafkaMessage(
                    topic=message.topic,
                    value=message.value,
                    key=(message.key.decode("utf-8", errors="ignore") if message.key else ""),
                    partition=message.partition,
                    offset=message.offset,
                    timestamp_ms=message.timestamp,
                )
        except Exception as exc:
            LOGGER.error(exc)
            raise
        finally:
            await consumer.stop()
