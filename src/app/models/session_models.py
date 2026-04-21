from datetime import datetime
from typing import Optional

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

class GameRecord:
    def __init__(self, bet_amount: float, outcome: str, stake_before: float, stake_after: float):
        self.timestamp = datetime.now()
        self.bet_amount = bet_amount
        self.outcome = outcome
        self.stake_before = stake_before
        self.stake_after = stake_after