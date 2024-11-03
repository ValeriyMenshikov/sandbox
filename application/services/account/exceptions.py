class AccountServiceError(Exception): ...


class AuthorizationError(AccountServiceError):
    """Raised when authorization fails."""

    message = "Authorization failed"


class EmailNotRegisteredError(AccountServiceError):
    """Raised when email is not registered for this account."""

    message = "Email is not registered for this account."
