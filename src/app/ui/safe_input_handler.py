from src.app.services.input_validator import InputValidator
from src.app.exceptions.validation_exceptions import ValidationException

class SafeInputHandler:
    def __init__(self):
        self.validator = InputValidator()

    def get_valid_stake(self, prompt: str) -> float:
        while True:
            user_input = input(prompt)
            try:
                val = self.validator.parse_and_validate_numeric(user_input, "Stake")
                self.validator.validate_initial_stake(val)
                return val
            except ValidationException as e:
                print(f"{e.error_type.value}: {e}")

    def get_valid_bet(self, prompt: str, current_stake: float) -> float:
        while True:
            user_input = input(prompt)
            try:
                val = self.validator.parse_and_validate_numeric(user_input, "Bet")
                self.validator.validate_bet_amount(val, current_stake)
                return val
            except ValidationException as e:
                print(f"{e.error_type.value}: {e}")