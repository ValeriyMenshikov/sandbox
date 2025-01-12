import json
from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from application.logger import LOGGER
from application.settings import Settings


@dataclass
class KafkaProducer:
    settings: Settings
    producer: AIOKafkaProducer = None

    async def connect(self) -> None:
        LOGGER.debug("Connecting to Kafka producer")
        await self.producer.start()

    async def disconnect(self) -> None:
        LOGGER.debug("Disconnecting from Kafka producer")
        await self.producer.stop()

    async def send(self, topic: str, message: dict) -> None:
        # TODO тут костыль потому что закрывается продюсер
        self.producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=[self.settings.KAFKA_URL],
        )
        try:
            await self.connect()
            await self.producer.send(topic, json.dumps(message).encode())
        except Exception as e:
            LOGGER.error(e)

        finally:
            await self.disconnect()
