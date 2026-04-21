import random
from typing import Optional
from src.app.db.connection import get_connection
from src.app.services.stake_management_service import StakeManagementService
from src.app.models.strategy import BettingStrategy

class BettingService:
    def __init__(self, stake_service: StakeManagementService):
        self.stake_service = stake_service
        self.session_id: Optional[int] = None

    def start_session(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO betting_sessions (gambler_id) VALUES (%s)"
        cursor.execute(query, (self.stake_service.gambler_id,))
        conn.commit()
        self.session_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return self.session_id

    def determine_outcome(self, probability: float) -> str:
        return "WIN" if random.random() <= probability else "LOSS"

    def place_bet(self, amount: float, probability: float, strategy_name: str = "Manual"):
        if not self.session_id:
            raise ValueError("Betting session not started.")
        
        if amount > self.stake_service.monitor.current_stake:
            raise ValueError("Insufficient stake for this bet.")

        stake_before = self.stake_service.monitor.current_stake
        
        # 1. Place bet (deduct amount)
        self.stake_service.process_bet_placed(amount, f"SES-{self.session_id}")
        
        # 2. Determine outcome
        outcome = self.determine_outcome(probability)
        
        # Potential Win = Bet Amount / Probability
        win_amount = (amount / probability) if outcome == "WIN" else 0.0
        status = self.stake_service.process_bet_outcome(win_amount, f"SES-{self.session_id}")
        
        stake_after = self.stake_service.monitor.current_stake

        # 4. Save to DB
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO bets (session_id, amount, probability, outcome, stake_before, stake_after, strategy_used)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (self.session_id, amount, probability, outcome, stake_before, stake_after, strategy_name))
        conn.commit()
        cursor.close()
        conn.close()

        return outcome, win_amount, status

    def place_consecutive_bets(self, num_bets: int, base_bet: float, probability: float, strategy: BettingStrategy):
        last_bet = base_bet
        last_outcome = None
        results = []

        for _ in range(num_bets):
            current_stake = self.stake_service.monitor.current_stake
            bet_amount = strategy.get_next_bet(current_stake, last_bet, last_outcome, base_bet)
            
            if bet_amount > current_stake:
                results.append("Stopped: Insufficient funds for next strategy step.")
                break

            outcome, win_amount, status = self.place_bet(bet_amount, probability, strategy.__class__.__name__)
            results.append(f"Bet: {bet_amount:.2f} -> {outcome} (Bal: {self.stake_service.monitor.current_stake:.2f})")
            
            last_bet = bet_amount
            last_outcome = outcome

        return results