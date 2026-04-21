Use Case 3. Betting Mechanism
Place a single bet with the specified amount
Determine bet outcome (win/loss) using probability
Apply bet amount to current stake based on outcome
Validate bet amount against current stake availability
Implement different betting strategies (fixed, percentage-based, progressive)
Handle multiple consecutive bets in a session
Key Components:
1. Bet Entity

Complete bet tracking with IDs, amounts, probabilities
Automatic potential win calculation based on odds
Tracks stake before/after each bet
Settlement logic for win/loss outcomes
2. Betting Strategies (5 implementations)

FixedAmountStrategy: Always bet the same amount
PercentageStrategy: Bet a percentage of current stake (e.g., 5%)
MartingaleStrategy: Double bet after each loss, reset to base after win
ReverseMartingaleStrategy: Double bet after each win, reset after loss
FibonacciStrategy: Progress through Fibonacci sequence on losses
D'AlembertStrategy: Gradually increase/decrease bet by fixed increment
3. BettingSession

Tracks all bets in a gaming session
Records start/end times and session statistics
Generates comprehensive session summaries
Links bets to their strategies
4. BettingService - Implements All Use Cases:

Place Single Bet: placeBet() with specified amount and win probability
Determine Outcome: determineBetOutcome() using random probability simulation
Apply to Stake: settleBet() automatically updates stake based on win/loss
Validate Amount: Built-in validation against current stake and min/max limits
Different Strategies: Multiple strategy implementations with placeBetWithStrategy()
Multiple Consecutive Bets: placeConsecutiveBets() handles session-based betting
Key Features:
Probability-based outcomes: Realistic win/loss determination using configurable probabilities
Automatic stake management: Stakes update automatically after each bet settlement
Strategy pattern: Easy to add new betting strategies
Comprehensive validation: Min/max bet limits, stake availability checks
Session tracking: Complete audit trail of all bets in a session
Odds calculation: Automatic potential win calculation based on probability
Real-time updates: Immediate stake updates and detailed logging
