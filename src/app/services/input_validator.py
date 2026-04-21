import math
from src.app.models.validation_models import ValidationConfig, ValidationResult
from src.app.exceptions.validation_exceptions import (
    ValidationException, StakeValidationException, 
    BetValidationException, LimitValidationException, 
    ProbabilityValidationException
)
from src.app.models.validation_enums import ValidationErrorType

class InputValidator:
    def __init__(self, config: ValidationConfig = None):
        self.config = config or ValidationConfig()

    def parse_and_validate_numeric(self, input_str: str, field_name: str) -> float:
        if input_str is None or str(input_str).strip() == "":
            raise ValidationException(f"{field_name} cannot be empty.", ValidationErrorType.NULL_ERROR, field_name, input_str)
        try:
            val = float(input_str)
            if math.isnan(val) or math.isinf(val):
                raise ValidationException(f"{field_name} cannot be NaN or Infinity.", ValidationErrorType.NUMERIC_ERROR, field_name, input_str)
            return val
        except ValueError:
            raise ValidationException(f"{field_name} must be a valid numeric value.", ValidationErrorType.NUMERIC_ERROR, field_name, input_str)

    def validate_initial_stake(self, stake: float):
        if stake < 0:
            raise StakeValidationException("Stake cannot be negative", "initial_stake", stake)
        if stake == 0 and not self.config.allow_zero_stake:
            raise StakeValidationException("Stake must be strictly positive", "initial_stake", stake)
        if stake < self.config.min_stake or stake > self.config.max_stake:
            raise StakeValidationException(f"Stake must be between {self.config.min_stake} and {self.config.max_stake}.", "initial_stake", stake)

    def validate_bet_amount(self, bet: float, current_stake: float):
        if bet <= 0:
            raise BetValidationException("Bet amount must be greater than zero.", "bet_amount", bet)
        if bet > current_stake:
            raise BetValidationException(f"Bet amount ({bet}) exceeds current available stake ({current_stake}).", "bet_amount", bet)
        if bet < self.config.min_bet or bet > self.config.max_bet:
            raise BetValidationException(f"Bet must be between {self.config.min_bet} and {self.config.max_bet}.", "bet_amount", bet)

    def validate_limits(self, lower_limit: float, upper_limit: float, initial_stake: float):
        if lower_limit < 0:
            raise LimitValidationException("Lower limit cannot be negative.", "lower_limit", lower_limit)
        if upper_limit <= lower_limit:
            raise LimitValidationException("Upper limit must be strictly greater than lower limit.", "limits", (lower_limit, upper_limit))
        if not (lower_limit <= initial_stake <= upper_limit):
            raise LimitValidationException("Initial stake must be between the lower and upper limits.", "limits", initial_stake)

    def validate_probability(self, prob: float):
        if prob < self.config.min_prob or prob > self.config.max_prob:
            raise ProbabilityValidationException(f"Probability must be between {self.config.min_prob} and {self.config.max_prob}.", "probability", prob)