from typing import Annotated

from aiochclient import ChClient
from fastapi import Depends
from redis.asyncio.client import Redis

from application.clients.http.base import Configuration
from application.clients.http.dm_api_account.apis.account_api import AccountApi
from application.clients.http.dm_api_account.apis.login_api import LoginApi
from application.clients.http.mailhog.apis.mailhog_api import MailhogApi
from application.clients.smtp.client import MailClient
from application.data_access.ch.access import get_ch_connection
from application.data_access.pg.access import get_repository
from application.data_access.redis.access import get_redis_connection
from application.services.account.repository.account_cache import AccountCache
from application.services.account.repository.account_repository import AccountRepository
from application.services.account.service import AccountService
from application.services.register.repository.register_analytics import RegisterAnalytics
from application.services.register.service import RegisterService
from application.services.users.repository.users_cache import UsersCache
from application.services.users.repository.users_repository import UsersRepository
from application.services.users.service import UsersService
from application.settings import Settings


def get_settings() -> Settings:
    return Settings()


async def get_http_account_api(
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> AccountApi:
    return AccountApi(Configuration(host=settings.HTTP_API_ACCOUNT, disable_log=settings.DISABLE_LOG))


async def get_http_login_api(
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> LoginApi:
    return LoginApi(Configuration(host=settings.HTTP_API_LOGIN, disable_log=settings.DISABLE_LOG))


async def get_mailhog_api(
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> MailhogApi:
    return MailhogApi(Configuration(host=settings.HTTP_MAILHOG, disable_log=settings.DISABLE_LOG))


async def account_cache_repository(
    redis_session: Annotated[Redis, Depends(get_redis_connection)],  # noqa: B008
) -> AccountCache:
    return AccountCache(redis=redis_session)


async def get_mail_client(
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> MailClient:
    return MailClient(settings=settings)


async def get_account_service(
    account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
    account_cache: AccountCache = Depends(account_cache_repository),  # noqa: B008
    mail_client: MailClient = Depends(get_mail_client),  # noqa: B008
    account_repository: AccountRepository = Depends(get_repository(AccountRepository)),  # noqa: B008
) -> AccountService:
    return AccountService(
        account_api=account_api,
        account_cache=account_cache,
        mail_client=mail_client,
        account_repository=account_repository,
    )


async def register_analytics_repository(
    ch_connection: Annotated[ChClient, Depends(get_ch_connection)],  # noqa: B008
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> RegisterAnalytics:
    return RegisterAnalytics(ch_client=ch_connection, settings=settings)


async def get_register_service(
    account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
    register_analytics: RegisterAnalytics = Depends(register_analytics_repository),  # noqa: B008
) -> RegisterService:
    return RegisterService(
        account_api=account_api,
        register_analytics=register_analytics,
    )


async def get_users_cache(
    redis_session: Annotated[Redis, Depends(get_redis_connection)],  # noqa: B008
) -> UsersCache:
    return UsersCache(
        redis=redis_session,
    )


async def get_users_service(
    users_repository: UsersRepository = Depends(get_repository(UsersRepository)),  # noqa: B008
    users_cache: UsersCache = Depends(get_users_cache),  # noqa: B008
) -> UsersService:
    return UsersService(
        users_repository=users_repository,
        users_cache=users_cache,
    )
