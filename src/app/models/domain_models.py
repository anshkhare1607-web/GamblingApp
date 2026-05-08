from datetime import datetime
from typing import Optional, List
from src.app.models.enums import TransactionType

class BettingPreferences:
    def __init__(self, max_bet, min_bet, game_type, auto_play, session_limit):
        self.max_bet = max_bet
        self.min_bet = min_bet
        self.game_type = game_type
        self.auto_play = auto_play
        self.session_limit = session_limit

class Gambler:
    def __init__(self, name, initial_stake, win_threshold, loss_threshold):
        self.name = name
        self.initial_stake = initial_stake
        self.current_stake = initial_stake
        self.win_threshold = win_threshold
        self.loss_threshold = loss_threshold
        self.total_bets = 0
        self.wins = 0
        self.losses = 0
        self.total_winnings = 0

class SessionParameters:
    def __init__(self, upper_limit: float, lower_limit: float, min_bet: float, max_bet: float, max_games: int, max_duration_sec: int, default_prob: float = 0.5):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.max_games = max_games
        self.max_duration_sec = max_duration_sec
        self.default_prob = default_prob

class PauseRecord:
    def __init__(self, reason: str):
        self.pause_time = datetime.now()
        self.resume_time: Optional[datetime] = None
        self.reason = reason
        
    def resume(self):
        self.resume_time = datetime.now()
        
    def get_duration_sec(self) -> float:
        end = self.resume_time if self.resume_time else datetime.now()
        return (end - self.pause_time).total_seconds()

class StakeBoundary:
    def __init__(self, min_stake: float, max_stake: float):
        self.min_stake = min_stake
        self.max_stake = max_stake
        self.warning_lower = min_stake * 1.20 
        self.warning_upper = max_stake * 0.80  
        
    def is_within_bounds(self, current_stake: float) -> bool:
        return self.min_stake <= current_stake <= self.max_stake
        
    def check_warnings(self, current_stake: float) -> str:
        if current_stake > self.max_stake: return "BREACHED: Upper stake limit exceeded."
        elif current_stake == self.max_stake: return "LIMIT REACHED: Upper stake limit."
        elif current_stake < self.min_stake: return "BREACHED: Lower stake limit exceeded."
        elif current_stake == self.min_stake: return "LIMIT REACHED: Lower stake limit."
        elif current_stake >= self.warning_upper: return "WARNING: Approaching upper stake limit."
        elif current_stake <= self.warning_lower: return "WARNING: Approaching lower stake limit."
        return "SAFE"

class StakeMonitor:
    def __init__(self, initial_stake: float):
        self.current_stake = initial_stake
        self.peak_stake = initial_stake
        self.lowest_stake = initial_stake
        self.history = [initial_stake]
        
    def update_stake(self, new_stake: float):
        self.current_stake = new_stake
        if new_stake > self.peak_stake: self.peak_stake = new_stake
        if new_stake < self.lowest_stake: self.lowest_stake = new_stake
        self.history.insert(0, new_stake)
        
    def calculate_volatility(self) -> float:
        if len(self.history) < 2: return 0.0
        changes = [abs(self.history[i] - self.history[i+1]) for i in range(len(self.history)-1)]
        return sum(changes) / len(changes)

class StakeTransaction:
    def __init__(self, amount: float, transaction_type: TransactionType, balance_after: float, bet_id: str = None):
        self.timestamp = datetime.now()
        self.amount = amount
        self.transaction_type = transaction_type
        self.balance_after = balance_after
        self.bet_id = bet_id

class StakeHistoryReport:
    def __init__(self, initial_balance: float, transactions: List[StakeTransaction]):
        self.initial_balance = initial_balance
        self.transactions = transactions
        
    def calculate_net_profit(self) -> float:
        if not self.transactions: return 0.0
        return self.transactions[-1].balance_after - self.initial_balance
        
    def get_transaction_history(self) -> List[StakeTransaction]:
        return self.transactions

class GameRecord:
    def __init__(self, bet_amount: float, outcome: str, stake_before: float, stake_after: float):
        self.timestamp = datetime.now()
        self.bet_amount = bet_amount
        self.outcome = outcome
        self.stake_before = stake_before
        self.stake_after = stake_after

class GameResult:
    def __init__(self, bet_amount: float, outcome: str, winnings: float, stake_before: float):
        self.timestamp = datetime.now()
        self.bet_amount = bet_amount
        self.outcome = outcome
        self.winnings = winnings if outcome == "WIN" else 0.0
        self.loss_amount = bet_amount if outcome == "LOSS" else 0.0
        self.stake_before = stake_before
        self.stake_after = stake_before + self.winnings - self.loss_amount

class RunningTotals:
    def __init__(self, initial_balance: float):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.total_wins = 0
        self.total_losses = 0
        self.total_winnings_amount = 0.0
        self.total_losses_amount = 0.0
        self.balance_history = [initial_balance]
        self.current_streak_type = None
        self.current_streak_count = 0
        self.longest_win_streak = 0
        self.longest_loss_streak = 0
        
    def update(self, result: GameResult):
        self.current_balance = result.stake_after
        self.balance_history.insert(0, self.current_balance)
        
        if result.outcome == "WIN":
            self.total_wins += 1
            self.total_winnings_amount += result.winnings
            self._update_streak("WIN")
        elif result.outcome == "LOSS":
            self.total_losses += 1
            self.total_losses_amount += result.loss_amount
            self._update_streak("LOSS")
            
    def _update_streak(self, outcome: str):
        if self.current_streak_type == outcome:
            self.current_streak_count += 1
        else:
            self.current_streak_type = outcome
            self.current_streak_count = 1
            
        if outcome == "WIN" and self.current_streak_count > self.longest_win_streak:
            self.longest_win_streak = self.current_streak_count
        elif outcome == "LOSS" and self.current_streak_count > self.longest_loss_streak:
            self.longest_loss_streak = self.current_streak_count
            
    def get_net_profit(self) -> float:
        return self.current_balance - self.initial_balance

class WinLossStatistics:
    def __init__(self, totals: RunningTotals):
        self.total_games = totals.total_wins + totals.total_losses
        self.wins = totals.total_wins
        self.losses = totals.total_losses
        self.win_rate = (self.wins / self.total_games * 100) if self.total_games > 0 else 0.0
        self.total_winnings = totals.total_winnings_amount
        self.total_losses = totals.total_losses_amount
        self.net_profit = totals.get_net_profit()
        self.avg_win = (self.total_winnings / self.wins) if self.wins > 0 else 0.0
        self.avg_loss = (self.total_losses / self.losses) if self.losses > 0 else 0.0
        self.profit_factor = (self.total_winnings / self.total_losses) if self.total_losses > 0 else float('inf')
        self.longest_win_streak = totals.longest_win_streak
        self.longest_loss_streak = totals.longest_loss_streak