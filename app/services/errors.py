class DomainError(Exception):
    """Base exception for predictable business failures."""


class NotFoundError(DomainError):
    pass


class InvalidTransitionError(DomainError):
    pass
