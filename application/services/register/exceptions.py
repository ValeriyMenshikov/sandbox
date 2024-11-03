class RegisterServiceError(Exception): ...


class RegistrationError(RegisterServiceError):
    """Raised when registration fails."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
