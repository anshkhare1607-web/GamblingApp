class BettingPreferences:
    def __init__(self, max_bet, min_bet, game_type, auto_play, session_limit):
        self.max_bet = max_bet
        self.min_bet = min_bet
        self.game_type = game_type
        self.auto_play = auto_play
        self.session_limit = session_limit