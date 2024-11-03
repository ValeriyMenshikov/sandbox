import dataclasses

import httpx

from application.clients.http.dm_api_account import AccountApi
from application.clients.http.dm_api_account.models.api_models import Registration
from application.services.register.exceptions import RegistrationError
from application.services.register.repository.register_analytics import RegisterAnalytics


@dataclasses.dataclass
class RegisterService:
    account_api: AccountApi
    register_analytics: RegisterAnalytics

    async def register(
        self,
        registration: Registration,
    ) -> None:
        try:
            await self.account_api.post_v1_account(registration=registration)
        except httpx.HTTPStatusError as e:
            if e.response.status_code:
                await self.register_analytics.set_event(
                    request_data=registration.json(),
                    status_code=e.response.status_code,
                    error_message=e.response.text,
                )
                raise RegistrationError(message=e.response.text) from e
        else:
            await self.register_analytics.set_event(
                request_data=registration.json(),
                status_code=201,
                error_message="",
            )
