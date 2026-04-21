Use Case 5. Win/Loss Calculation
Determine random or probability-based game outcomes
Calculate winnings based on bet amount and odds
Calculate losses and deduct from stake
Maintain running total of wins and losses
Compute win/loss ratio for session
Track consecutive wins and losses
Key Components:
1. Outcome Strategies (Multiple Implementations)

RandomOutcomeStrategy: Pure random outcomes based on probability
WeightedProbabilityStrategy: Includes house edge for realistic casino simulation
2. Odds Configuration System

Supports multiple odds types:

FIXED: Simple multiplier (e.g., 2x your bet)
PROBABILITY_BASED: Winnings calculated from win probability (lower probability = higher payout)
AMERICAN: American odds format (negative for favorites, positive for underdogs)
DECIMAL: European decimal odds format
3. GameResult Class

Records complete game information
Calculates winnings based on odds configuration
Tracks stake changes before/after each game
Provides detailed result formatting
4. WinLossStatistics Class Comprehensive statistical analysis:

Win/loss/push counts and rates
Total winnings and losses
Average win/loss amounts
Profit factor calculation
Largest win/loss tracking
Streak analysis (current and longest)
Performance metrics

5. RunningTotals Class

Real-time cumulative tracking
Balance history for every game
Profit/loss progression over time
Net profit/loss calculation
6. WinLossCalculator Service

Implements all 6 use cases:
Determine Outcomes: Multiple strategies (random, weighted with house edge)
Calculate Winnings: Automatic calculation based on bet amount and odds configuration
Calculate Losses: Automatic deduction from stake
Maintain Running Totals: Real-time tracking of cumulative wins/losses and balance
Compute Win/Loss Ratio: Instant calculation of ratios and win rates
Track Consecutive Streaks: Current and longest win/loss streaks
Key Features:
Multiple Outcome Strategies: Random, weighted probability with house edge
Flexible Odds Systems: Fixed, probability-based, American, decimal
Comprehensive Statistics: 15+ different metrics tracked
Real-time Tracking: Running totals updated after each game
Streak Detection: Automatic tracking of current and longest streaks
Balance History: Complete progression tracking
Profit Factor: Ratio of total winnings to total losses
Performance Metrics: Win rate, ROI, return on risk
