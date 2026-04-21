from abc import ABC, abstractmethod

class BettingStrategy(ABC):
    @abstractmethod
    def get_next_bet(self, current_stake: float, last_bet: float, last_outcome: str, base_bet: float) -> float:
        pass

class FixedAmountStrategy(BettingStrategy):
    def get_next_bet(self, current_stake: float, last_bet: float, last_outcome: str, base_bet: float) -> float:
        return base_bet

class PercentageStrategy(BettingStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def get_next_bet(self, current_stake: float, last_bet: float, last_outcome: str, base_bet: float) -> float:
        return current_stake * (self.percentage / 100)

class MartingaleStrategy(BettingStrategy):
    def get_next_bet(self, current_stake: float, last_bet: float, last_outcome: str, base_bet: float) -> float:
        if last_outcome == "LOSS":
            return last_bet * 2
        return base_bet

class ReverseMartingaleStrategy(BettingStrategy):
    def get_next_bet(self, current_stake: float, last_bet: float, last_outcome: str, base_bet: float) -> float:
        if last_outcome == "WIN":
            return last_bet * 2
        return base_bet

class FibonacciStrategy(BettingStrategy):
    def __init__(self):
        self.sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        self.index = 0

    def get_next_bet(self, current_stake: float, last_bet: float, last_outcome: str, base_bet: float) -> float:
        if last_outcome == "LOSS":
            self.index = min(self.index + 1, len(self.sequence) - 1)
        elif last_outcome == "WIN":
            self.index = max(0, self.index - 2)
        return base_bet * self.sequence[self.index]

class DAlembertStrategy(BettingStrategy):
    def __init__(self, increment: float):
        self.increment = increment

    def get_next_bet(self, current_stake: float, last_bet: float, last_outcome: str, base_bet: float) -> float:
        if not last_outcome:
            return base_bet
        if last_outcome == "LOSS":
            return last_bet + self.increment
        return max(base_bet, last_bet - self.increment)