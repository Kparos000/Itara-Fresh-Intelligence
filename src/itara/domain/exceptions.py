"""Domain-specific exceptions for Itara Fresh Intelligence."""


class ItaraDomainError(ValueError):
    """Base exception for invalid Itara domain state."""


class InvalidCoordinateError(ItaraDomainError):
    """Raised when a latitude or longitude value is outside valid bounds."""


class InvalidFinancialValueError(ItaraDomainError):
    """Raised when a financial value is invalid."""


class InvalidRelationshipError(ItaraDomainError):
    """Raised when domain relationships are inconsistent."""
