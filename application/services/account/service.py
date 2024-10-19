import dataclasses

from application.clients.http.dm_api_account import AccountApi
from application.clients.http.dm_api_account.models.api_models import UserDetailsEnvelope
from application.services.account.repository.cache_details import AccountCache


@dataclasses.dataclass
class AccountService:
    account_api: AccountApi
    account_cache: AccountCache

    async def get_info(self, token) -> UserDetailsEnvelope:
        login = await self.account_cache.get_login(token)
        if not login:
            response = await self.account_api.get_v1_account(x_dm_auth_token=token)
            login = response.resource.login
            await self.account_cache.set_login(token=token, login=login)
            await self.account_cache.set_account_info(user_details=response)
        else:
            response = await self.account_cache.get_account_info(login=login)
        return response

    async def update_info(self, token: str) -> None:
        user_data = await self.account_api.get_v1_account(x_dm_auth_token=token)
        # TODO: тут логика обновления информации о пользователе
        login = user_data.resource.login  # noqa: F841
        return
