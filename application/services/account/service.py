import dataclasses
import uuid

import httpx

from application.clients.http.dm_api_account import AccountApi
from application.clients.http.dm_api_account.models.api_models import UserDetailsEnvelope, UserEnvelope
from application.clients.smtp.client import MailClient
from application.services.account.exceptions import AuthorizationError, EmailNotRegisteredError
from application.services.account.repository.account_cache import AccountCache
from application.services.account.repository.account_repository import AccountRepository
from application.services.account.schema import UserSchema


@dataclasses.dataclass
class AccountService:
    account_api: AccountApi
    account_cache: AccountCache
    mail_client: MailClient
    account_repository: AccountRepository

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

    async def update_info(self, token: str, user: UserSchema) -> UserDetailsEnvelope:
        response = await self._user_info_by_token(token=token)
        login = response.resource.login  # noqa: F841
        await self.account_repository.update_user(user_login=login, user=user)
        updated_user_data = await self.account_api.get_v1_account(x_dm_auth_token=token)
        return updated_user_data

    async def reset_password(self, reset_password_model) -> UserEnvelope:
        return await self.account_api.post_v1_account_password(reset_password=reset_password_model)

    async def change_password(self, change_password_model) -> UserEnvelope:
        return await self.account_api.put_v1_account_password(change_password=change_password_model)

    async def change_email(self, change_mail_model) -> UserEnvelope:
        return await self.account_api.put_v1_account_email(change_email=change_mail_model)

    async def delete_account(self, token, email) -> None:
        response = await self._user_info_by_token(token=token)

        dataset = await self.account_repository.get_user(login=response.resource.login)
        if dataset.Email != email:
            raise EmailNotRegisteredError

        delete_token = uuid.uuid4()
        await self.mail_client.send_email(
            subject="Delete account",
            text=f"Token for delete your account: {delete_token}, expires in 5 minutes",
            to=email,
        )
        await self.account_cache.set_delete_account_token(token=token, delete_token=str(delete_token).encode("utf-8"))

    async def delete_account_by_token(self, token, delete_token) -> str:
        response = await self._user_info_by_token(token=token)

        confirmation_token = await self.account_cache.get_delete_account_token(token=token)
        if confirmation_token == delete_token:
            await self.account_repository.delete_account(login=response.resource.login)
            return "ok"
        return "error"

    async def _user_info_by_token(self, token: str) -> UserDetailsEnvelope:
        try:
            response = await self.account_api.get_v1_account(x_dm_auth_token=token)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthorizationError from e
        else:
            return response
