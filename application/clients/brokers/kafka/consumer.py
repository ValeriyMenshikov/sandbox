import abc
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer

from application.clients.http.dm_api_account.models.api_models import Registration
from application.services.register.service import RegisterService


@dataclass
class BaseConsumer(abc.ABC):
    consumer: AIOKafkaConsumer
    register_service: RegisterService

    async def open_connection(self) -> None:
        await self.consumer.start()

    async def close_connection(self) -> None:
        await self.consumer.stop()


class KafkaRegisterConsumer(BaseConsumer):
    consumer: AIOKafkaConsumer
    register_service: RegisterService

    async def registration_consume(self) -> None:
        await self.open_connection()
        try:
            async for message in self.consumer:
                try:
                    await self.register_service.register(registration=Registration.model_validate(message.value))
                except Exception as e:
                    print(e)
        finally:
            await self.close_connection()


class KafkaRetryRegisterConsumer(BaseConsumer):
    consumer: AIOKafkaConsumer
    register_service: RegisterService

    async def registration_consume(self) -> None:
        await self.open_connection()
        try:
            async for message in self.consumer:
                print("error", message.value)
                try:
                    if message.value["error_type"] != "validation":
                        print("error", message.value)
                        await self.register_service.register(
                            registration=Registration.model_validate(message.value["input_data"])
                        )
                except Exception as e:
                    print(e)
        finally:
            await self.close_connection()
