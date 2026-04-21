from datetime import datetime

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
        
        # Streak tracking
        self.current_streak_type = None
        self.current_streak_count = 0
        self.longest_win_streak = 0
        self.longest_loss_streak = 0

    def update(self, result: GameResult):
        self.current_balance = result.stake_after
        self.balance_history.append(self.current_balance)
        
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
        
        # Profit Factor: Gross Profit / Gross Loss
        self.profit_factor = (self.total_winnings / self.total_losses) if self.total_losses > 0 else float('inf')
        
        self.longest_win_streak = totals.longest_win_streak
        self.longest_loss_streak = totals.longest_loss_streak