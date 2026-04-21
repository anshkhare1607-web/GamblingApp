class ValidationResult:
    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []

    def add_error(self, message: str):
        self.is_valid = False
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

class ValidationConfig:
    def __init__(self):
        self.min_stake = 1.0
        self.max_stake = 1000000.0
        self.min_bet = 1.0
        self.max_bet = 50000.0
        self.min_prob = 0.01
        self.max_prob = 1.0
        self.strict_mode = True
        self.allow_zero_stake = False