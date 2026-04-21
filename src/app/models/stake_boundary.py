class StakeBoundary:
    def __init__(self, min_stake: float, max_stake: float):
        self.min_stake = min_stake
        self.max_stake = max_stake
        self.warning_lower = min_stake * 1.20 
        self.warning_upper = max_stake * 0.80  

    def is_within_bounds(self, current_stake: float) -> bool:
        return self.min_stake <= current_stake <= self.max_stake

    def check_warnings(self, current_stake: float) -> str:
        if current_stake > self.max_stake:
            return "BREACHED: Upper stake limit exceeded."
        elif current_stake == self.max_stake:
            return "LIMIT REACHED: Upper stake limit."
        elif current_stake < self.min_stake:
            return "BREACHED: Lower stake limit exceeded."
        elif current_stake == self.min_stake:
            return "LIMIT REACHED: Lower stake limit."
        elif current_stake >= self.warning_upper:
            return "WARNING: Approaching upper stake limit."
        elif current_stake <= self.warning_lower:
            return "WARNING: Approaching lower stake limit."
        return "SAFE"