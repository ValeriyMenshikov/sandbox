from application.register.app import app as register_app
from application.users.app import app as user_app
from application.auth.app import app as auth_app
from application.mail.app import app as mail_app

APP_MAP = {
    "register": register_app,
    "users": user_app,
    "auth": auth_app,
    "mail": mail_app
}
