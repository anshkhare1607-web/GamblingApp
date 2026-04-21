class StakeMonitor:
    def __init__(self, initial_stake: float):
        self.current_stake = initial_stake
        self.peak_stake = initial_stake
        self.lowest_stake = initial_stake
        self.history = [initial_stake]

    def update_stake(self, new_stake: float):
        self.current_stake = new_stake
        if new_stake > self.peak_stake:
            self.peak_stake = new_stake
        if new_stake < self.lowest_stake:
            self.lowest_stake = new_stake
        self.history.append(new_stake)

    def calculate_volatility(self) -> float:
        if len(self.history) < 2:
            return 0.0
        changes = [abs(self.history[i] - self.history[i-1]) for i in range(1, len(self.history))]
        return sum(changes) / len(changes)