from application.clients.http.dm_api_account.apis.account_api import AccountApi
from application.clients.http.dm_api_account.apis.login_api import LoginApi
from application.clients.http.mailhog.apis.mailhog_api import MailhogApi
from application.clients.http.base import Configuration
from fastapi import Depends


class Settings:
    account_api: str = "http://5.63.153.31:5051/"
    login_api: str = "http://5.63.153.31:5051/"
    mailhog_api: str = "http://5.63.153.31:5025/"


# def get_settings():
#     cfg = Configuration(host="http://5.63.153.31:5051/")
#     return cfg


async def get_http_account_api(
        # settings=Depends(get_settings)
) -> AccountApi:
    return AccountApi(Configuration(host=Settings.account_api))


async def get_http_login_api(
        # settings=Depends(get_settings)
) -> LoginApi:
    return LoginApi(Configuration(host=Settings.login_api))


async def get_mailhog_api(
        # settings=Depends(get_settings)
) -> MailhogApi:
    return MailhogApi(Configuration(host=Settings.mailhog_api))
