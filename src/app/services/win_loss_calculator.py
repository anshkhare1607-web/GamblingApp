from src.app.models.odds import OddsType, OddsCalculator
from src.app.models.outcome_strategy import OutcomeStrategy
from src.app.models.statistics_models import GameResult, RunningTotals, WinLossStatistics
from src.app.db.connection import get_connection

class WinLossCalculator:
    def __init__(self, session_id: int, initial_stake: float, outcome_strategy: OutcomeStrategy):
        self.session_id = session_id
        self.outcome_strategy = outcome_strategy
        self.totals = RunningTotals(initial_stake)
        self.results = []

    def process_game(self, bet_amount: float, odds_type: OddsType, odds_value: float, win_probability: float = 0.5) -> GameResult:
        if bet_amount > self.totals.current_balance:
            raise ValueError("Insufficient funds for this bet.")

        # 1. Determine Outcome
        outcome = self.outcome_strategy.determine_outcome(win_probability)

        # 2. Calculate Winnings/Losses
        if outcome == "WIN":
            winnings = OddsCalculator.calculate_winnings(bet_amount, odds_type, odds_value)
        else:
            winnings = 0.0

        # 3. Create Result Record
        result = GameResult(bet_amount, outcome, winnings, self.totals.current_balance)
        self.results.append(result)

        # 4. Maintain Running Totals
        self.totals.update(result)

        return result

    def generate_statistics(self) -> WinLossStatistics:
        return WinLossStatistics(self.totals)

    def save_statistics(self, gambler_id: int):
        stats = self.generate_statistics()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO session_statistics 
        (session_id, gambler_id, total_games, wins, losses, total_winnings, total_losses, 
         net_profit, win_rate, longest_win_streak, longest_loss_streak, profit_factor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            self.session_id, gambler_id, stats.total_games, stats.wins, stats.losses,
            stats.total_winnings, stats.total_losses, stats.net_profit, stats.win_rate,
            stats.longest_win_streak, stats.longest_loss_streak, stats.profit_factor
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()