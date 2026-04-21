from src.app.models.validation_enums import ValidationErrorType

class ValidationException(Exception):
    def __init__(self, message: str, error_type: ValidationErrorType, field: str = None, value: any = None):
        super().__init__(message)
        self.error_type = error_type
        self.field = field
        self.value = value

class StakeValidationException(ValidationException):
    def __init__(self, message: str, field: str = None, value: any = None):
        super().__init__(message, ValidationErrorType.STAKE_ERROR, field, value)

class BetValidationException(ValidationException):
    def __init__(self, message: str, field: str = None, value: any = None):
        super().__init__(message, ValidationErrorType.BET_ERROR, field, value)

class LimitValidationException(ValidationException):
    def __init__(self, message: str, field: str = None, value: any = None):
        super().__init__(message, ValidationErrorType.LIMIT_ERROR, field, value)

class ProbabilityValidationException(ValidationException):
    def __init__(self, message: str, field: str = None, value: any = None):
        super().__init__(message, ValidationErrorType.PROBABILITY_ERROR, field, value)