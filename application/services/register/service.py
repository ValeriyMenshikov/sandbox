import dataclasses
import json

import httpx

from application.clients.brokers.kafka.producer import KafkaProducer
from application.clients.http.dm_api_account import AccountApi
from application.clients.http.dm_api_account.models.api_models import Registration
from application.services.register.exceptions import RegistrationError
from application.services.register.repository.register_analytics import RegisterAnalytics


@dataclasses.dataclass
class RegisterService:
    account_api: AccountApi
    register_analytics: RegisterAnalytics
    kafka_producer: KafkaProducer

    async def register(
        self,
        registration: Registration,
    ) -> None:
        try:
            await self.account_api.post_v1_account_with_http_info(registration=registration)
        except httpx.HTTPStatusError as e:
            if e.response.status_code:
                message = {
                    "input_data": json.loads(registration.model_dump_json()),
                    "error_message": e.response.json(),
                    "error_type": "validation",
                }
                await self.register_analytics.set_event(
                    request_data=registration.json(),
                    status_code=e.response.status_code,
                    error_message=e.response.text,
                )
                await self.kafka_producer.send(topic="register-events-errors", message=message)
                raise RegistrationError(message=e.response.text) from e
        except Exception as e:
            message = {
                "input_data": json.loads(registration.model_dump_json()),
                "error_message": str(e),
                "error_type": "unknown",
            }
            await self.kafka_producer.send(topic="register-events-errors", message=message)
        else:
            await self.register_analytics.set_event(
                request_data=registration.json(),
                status_code=201,
                error_message="",
            )
