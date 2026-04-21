Use Case 4. Game Session Management
Start new gambling session with initial parameters
Continue session while stake remains within boundaries
Pause and resume gaming sessions
End session when upper limit reached (win condition)
End session when lower limit reached (loss condition)
Track session duration and number of games played
Key Components:
1. SessionStatus & SessionEndReason Enums

Tracks all possible session states (INITIALIZED, ACTIVE, PAUSED, ENDED_WIN, ENDED_LOSS, etc.)
Captures why sessions end (upper limit, lower limit, manual, timeout)
2. GameRecord Class

Records each individual game played
Tracks bet amount, outcome, stake changes, and duration
Links games to their session
3. SessionParameters Class

Configurable session limits (upper/lower boundaries)
Min/max bet amounts
Maximum games and session duration
Default win probability
Automatic boundary validation
4. PauseRecord Class

Tracks each pause/resume cycle
Records pause duration and reason
Maintains complete pause history
5. GamingSession Class Implements all core functionality:

Start: Initialize session with parameters and timestamp
Play Games: Execute games with automatic outcome determination
Pause/Resume: Full pause functionality with duration tracking
Boundary Monitoring: Continuous checking of stake limits
Auto-End: Automatically ends when upper/lower limits reached
Duration Tracking: Separates active time from paused time
Statistics: Complete game statistics and session summary
6. GameSessionManager Manages multiple sessions:

Prevents duplicate active sessions per gambler
Handles session lifecycle (start, pause, resume, end)
Tracks active and completed sessions
Provides session retrieval and reporting
All Use Cases Implemented:
Start New Session: startNewSession() with initial parameters validation
Continue Session: continueSession() plays multiple games while checking boundaries after each game
Pause/Resume: Full pause functionality with reason tracking and duration calculation
End on Upper Limit: Automatic detection and session end when win threshold reached
End on Lower Limit: Automatic detection and session end when loss threshold reached
Track Duration & Games: Complete tracking of:
Total session duration
Active play duration
Pause duration
Number of games played
Win/loss statistics
Game-by-game history
Key Features:
Automatic Boundary Detection: Sessions end immediately when limits are reached
Comprehensive Pause System: Multiple pause/resume cycles with full tracking
Real-time Monitoring: Continuous validation during gameplay
Session Timeout Protection: Prevents excessively long sessions
Detailed Statistics: Win rate, average bet, ROI, duration breakdowns
Complete Audit Trail: Every game and pause is recorded
