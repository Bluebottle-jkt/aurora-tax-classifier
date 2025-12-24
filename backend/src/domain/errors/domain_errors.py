"""
Domain-level errors and exceptions.
Pure domain layer - no framework dependencies.
"""


class DomainError(Exception):
    """Base class for all domain errors"""
    pass


class DomainValidationError(DomainError):
    """Raised when domain validation fails"""
    pass


class InvalidTaxObjectLabelError(DomainValidationError):
    """Raised when an invalid tax object label is provided"""
    pass


class InvalidConfidenceScoreError(DomainValidationError):
    """Raised when confidence score is out of valid range"""
    pass


class InvalidRiskScoreError(DomainValidationError):
    """Raised when risk score is out of valid range"""
    pass


class InvalidJobStatusError(DomainValidationError):
    """Raised when job status transition is invalid"""
    pass


class MissingRequiredFieldError(DomainValidationError):
    """Raised when a required field is missing"""
    pass


class InvalidBusinessTypeError(DomainValidationError):
    """Raised when business type is not recognized"""
    pass
