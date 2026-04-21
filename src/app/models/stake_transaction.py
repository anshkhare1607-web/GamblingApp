from enum import Enum
from datetime import datetime

class TransactionType(Enum):
    INITIAL_STAKE = "INITIAL_STAKE"
    BET_PLACED = "BET_PLACED"
    BET_WIN = "BET_WIN"
    BET_LOSS = "BET_LOSS"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    ADJUSTMENT = "ADJUSTMENT"
    RESET = "RESET"

class StakeTransaction:
    def __init__(self, amount: float, transaction_type: TransactionType, balance_after: float, bet_id: str = None):
        self.timestamp = datetime.now()
        self.amount = amount
        self.transaction_type = transaction_type
        self.balance_after = balance_after
        self.bet_id = bet_id