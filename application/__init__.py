from application.services.register.app import app as register_app
from application.services.users.app import app as user_app
from application.services.auth.app import app as auth_app
from application.services.mail.app import app as mail_app
from application.services.account.app import app as account_app
from application.services.broker.app import app as broker_app
from application.logger import LOGGER

APP_MAP = {
    "register": register_app,
    "users": user_app,
    "auth": auth_app,
    "mail": mail_app,
    "account": account_app,
    "broker": broker_app,
}
