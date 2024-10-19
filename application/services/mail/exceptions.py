class MailhogError(Exception): ...


class MailNotFoundError(MailhogError):
    message = "Message not found"
