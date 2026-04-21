from typing import List
from src.app.models.stake_transaction import StakeTransaction, TransactionType
from src.app.models.stake_boundary import StakeBoundary
from src.app.services.stake_monitor import StakeMonitor
from src.app.models.stake_history_report import StakeHistoryReport
from src.app.db.connection import get_connection

class StakeManagementService:
    def __init__(self, gambler_id: int, initial_stake: float, min_limit: float, max_limit: float):
        self.gambler_id = gambler_id
        self.boundary = StakeBoundary(min_limit, max_limit)
        
        if not self.boundary.is_within_bounds(initial_stake):
            raise ValueError("Initial stake is outside boundaries")
        
        self.monitor = StakeMonitor(initial_stake)
        self.transactions: List[StakeTransaction] = []
        self._record_transaction(initial_stake, TransactionType.INITIAL_STAKE, initial_stake)

    def _record_transaction(self, amount: float, t_type: TransactionType, balance: float, bet_id: str = None):
        # 1. Store in memory for immediate session reporting
        transaction = StakeTransaction(amount, t_type, balance, bet_id)
        self.transactions.append(transaction)
        
        # 2. Persist to Database
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO stake_transactions 
        (gambler_id, timestamp, amount, transaction_type, balance_after, bet_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (self.gambler_id, transaction.timestamp, amount, t_type.value, balance, bet_id)
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()

    def process_bet_placed(self, amount: float, bet_id: str):
        new_balance = self.monitor.current_stake - amount
        self.monitor.update_stake(new_balance)
        self._record_transaction(amount, TransactionType.BET_PLACED, new_balance, bet_id)
        return self.boundary.check_warnings(new_balance)

    def process_bet_outcome(self, amount_won: float, bet_id: str):
        new_balance = self.monitor.current_stake + amount_won
        t_type = TransactionType.BET_WIN if amount_won > 0 else TransactionType.BET_LOSS
        self.monitor.update_stake(new_balance)
        self._record_transaction(amount_won, t_type, new_balance, bet_id)
        return self.boundary.check_warnings(new_balance)

    def generate_report(self) -> StakeHistoryReport:
        initial = self.transactions[0].amount if self.transactions else 0.0
        return StakeHistoryReport(initial, self.transactions)