class GamblerStatistics:
    def __init__(self, data):
        self.name = data['name']
        self.current_stake = data['current_stake']
        self.initial_stake = data['initial_stake']
        self.total_bets = data['total_bets']
        self.wins = data['wins']
        self.losses = data['losses']

    def win_rate(self):
        if self.total_bets == 0:
            return 0
        return (self.wins / self.total_bets) * 100

    def net_profit(self):
        return self.current_stake - self.initial_stake

    def threshold_status(self, win_threshold, loss_threshold):
        if self.current_stake >= win_threshold:
            return "WIN LIMIT REACHED"
        elif self.current_stake <= loss_threshold:
            return "LOSS LIMIT REACHED"
        return "ACTIVE"