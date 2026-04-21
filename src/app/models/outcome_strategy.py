from abc import ABC, abstractmethod
import random

class OutcomeStrategy(ABC):
    @abstractmethod
    def determine_outcome(self, win_probability: float) -> str:
        pass

class RandomOutcomeStrategy(OutcomeStrategy):
    def determine_outcome(self, win_probability: float) -> str:
        return "WIN" if random.random() <= win_probability else "LOSS"

class WeightedProbabilityStrategy(OutcomeStrategy):
    def __init__(self, house_edge_percentage: float):
        self.house_edge = house_edge_percentage / 100.0

    def determine_outcome(self, win_probability: float) -> str:
        # Reduces the player's true win probability by the house edge
        actual_probability = win_probability * (1.0 - self.house_edge)
        return "WIN" if random.random() <= actual_probability else "LOSS"