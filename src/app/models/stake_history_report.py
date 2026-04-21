from typing import List
from src.app.models.stake_transaction import StakeTransaction

class StakeHistoryReport:
    def __init__(self, initial_balance: float, transactions: List[StakeTransaction]):
        self.initial_balance = initial_balance
        self.transactions = transactions

    def calculate_net_profit(self) -> float:
        if not self.transactions:
            return 0.0
        return self.transactions[-1].balance_after - self.initial_balance

    def get_transaction_history(self) -> List[StakeTransaction]:
        return self.transactions