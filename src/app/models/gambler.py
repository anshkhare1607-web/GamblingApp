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