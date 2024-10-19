import dataclasses

from application.clients.http.dm_api_account import AccountApi


@dataclasses.dataclass
class AccountService:
    account_api: AccountApi

    async def update_info(self, token: str) -> None:
        user_data = await self.account_api.get_v1_account(x_dm_auth_token=token)
        # TODO: тут логика обновления информации о пользователе
        login = user_data.resource.login  # noqa: F841
        return
