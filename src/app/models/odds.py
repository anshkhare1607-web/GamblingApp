from enum import Enum

class OddsType(Enum):
    FIXED = "FIXED"
    PROBABILITY_BASED = "PROBABILITY_BASED"
    AMERICAN = "AMERICAN"
    DECIMAL = "DECIMAL"

class OddsCalculator:
    @staticmethod
    def calculate_winnings(bet_amount: float, odds_type: OddsType, odds_value: float) -> float:
        if odds_type == OddsType.FIXED:
            # odds_value acts as a simple multiplier (e.g., 2.0x)
            return bet_amount * odds_value
        
        elif odds_type == OddsType.PROBABILITY_BASED:
            # Lower probability = higher payout. e.g., 0.25 prob = 4x payout
            if odds_value <= 0 or odds_value > 1:
                raise ValueError("Probability must be between 0.01 and 1.0")
            return bet_amount * (1 / odds_value)
            
        elif odds_type == OddsType.AMERICAN:
            # Positive for underdog (e.g., +150 means $150 profit on $100 bet)
            # Negative for favorite (e.g., -150 means $100 profit on $150 bet)
            if odds_value > 0:
                return bet_amount * (odds_value / 100) + bet_amount
            elif odds_value < 0:
                return bet_amount * (100 / abs(odds_value)) + bet_amount
            else:
                return bet_amount # push/even
                
        elif odds_type == OddsType.DECIMAL:
            # Standard European decimal odds (e.g., 2.50)
            return bet_amount * odds_value
        
        return 0.0