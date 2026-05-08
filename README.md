# GamblingApp

GamblingApp is a command-line interface (CLI) based gambling simulation application built in Python. It allows users to create gambler profiles, manage betting sessions with predefined limits and thresholds, and simulate gambling games with real-time stake tracking and session management. The application uses MySQL for data persistence and includes robust input validation, session controls, and comprehensive statistics tracking.

## Features

- **Gambler Profile Management**: Create and manage gambler profiles with initial stakes, win/loss thresholds, and betting preferences
- **Session-Based Gaming**: Start managed gambling sessions with configurable parameters including stake limits, bet ranges, and time constraints
- **Real-Time Stake Tracking**: Monitor current stake levels and session status in real-time
- **Betting Controls**: Place bets within defined limits with automatic validation
- **Session Management**: Pause, resume, and end sessions manually or automatically based on thresholds
- **Statistics & Reporting**: View detailed session summaries including wins, losses, and total winnings
- **MySQL Persistence**: All gambler data, sessions, and bets are stored in a MySQL database
- **Input Validation**: Comprehensive validation for all user inputs with custom exception handling
- **Modular Architecture**: Well-organized codebase with separate modules for database, models, services, and UI

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GamblingApp
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables by creating a `.env` file in the root directory:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=gambling_db
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

4. Ensure MySQL server is running and the database exists.

## Usage

Run the application:
```bash
python src/app/main.py
```

### Main Menu Options:
- **0. Create New Gambler Profile**: Set up a new gambler with name, initial stake, thresholds, and betting preferences
- **1. Start Managed Session**: Begin a new gambling session with predefined parameters
- **2. Play Next Game**: Place a bet and simulate a game outcome
- **3. View Real-Time Status**: Check current stake and session status
- **4. End Session & View Summary**: Terminate session and view final statistics
- **5. Pause / Resume Session**: Temporarily halt or continue an active session
- **6. Exit**: Close the application

## Project Structure

```
GamblingApp/
├── README.md
├── requirements.txt
├── src/
│   └── app/
│       ├── main.py                 # Application entry point
│       ├── config/
│       │   └── settings.py         # Database configuration
│       ├── db/
│       │   └── database.py         # MySQL database setup and connections
│       ├── exceptions/
│       │   └── validation_exceptions.py  # Custom validation errors
│       ├── models/
│       │   ├── domain_models.py    # Core business objects
│       │   ├── enums.py            # Enumeration types
│       │   └── strategy.py         # Betting strategies
│       ├── services/
│       │   ├── betting_service.py          # Betting logic
│       │   ├── gambler_service.py          # Gambler management
│       │   ├── game_session_manager.py     # Session handling
│       │   ├── input_validator.py          # Input validation
│       │   ├── stake_management_service.py # Stake controls
│       │   └── win_loss_calculator.py      # Outcome calculations
│       └── ui/
│           └── cli_interface.py     # Command-line interface
└── tests/                          # Test directory (currently empty)
```


## Database Schema

The application creates three main tables:
- **gambler**: Stores gambler profiles and preferences
- **betting_sessions**: Tracks gambling sessions with start/end times and status
- **bets**: Records individual bets with amounts, outcomes, and stake changes

