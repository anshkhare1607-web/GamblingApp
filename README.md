Use Case 1. Gambler Profile Management
Create new gambler with initial stake, win threshold, and loss threshold
Update gambler personal information and betting preferences
Retrieve gambler statistics and current financial status
Validate gambler eligibility based on minimum stake requirements
Reset gambler profile to initial state for new gaming session
Key Components:

1. GamblerProfile Entity

Stores all gambler information including personal details, financial data, and betting history
Tracks initial stake, current stake, win/loss thresholds
Records statistics like total bets, wins, losses, winnings
2. BettingPreferences Class

Manages gambler's betting preferences (max/min bet amounts, preferred game type, auto-play settings, session limits)
3. GamblerStatistics DTO

Provides comprehensive statistics including win rate, net profit/loss, average bet amount
Checks threshold status
4. GamblerProfileService

Implements all five use cases:
Create: Validates minimum stake and threshold requirements
Update: Supports updating personal info, preferences, and thresholds
Retrieve: Returns detailed statistics and financial status
Validate: Checks eligibility based on stake requirements, thresholds, and account status
Reset: Resets profile for new session with proportional threshold adjustments
5. Demo Application

Shows complete workflow with examples of all operations
Features:

Input validation for all operations
Timestamp tracking for audit trail
Proportional threshold calculation when resetting
Comprehensive error handling
Helper methods for bet recording and account deactivation
