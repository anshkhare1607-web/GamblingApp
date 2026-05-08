import mysql.connector
from src.app.config.settings import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def setup_all_tables():
    conn = get_connection()
    cursor = conn.cursor()

    queries = [
        """
        CREATE TABLE IF NOT EXISTS gambler (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            initial_stake DECIMAL(10,2),
            current_stake DECIMAL(10,2),
            win_threshold DECIMAL(10,2),
            loss_threshold DECIMAL(10,2),
            total_bets INT,
            wins INT,
            losses INT,
            max_bet DECIMAL(10,2),
            min_bet DECIMAL(10,2),
            game_type VARCHAR(50),
            auto_play BOOLEAN,
            session_limit INT
        ) ;
        """,
        """
        CREATE TABLE IF NOT EXISTS betting_sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gambler_id INT NOT NULL,
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATETIME NULL,
            status VARCHAR(20) DEFAULT 'ACTIVE',
            FOREIGN KEY (gambler_id) REFERENCES gambler(id) ON DELETE CASCADE
        ) ;
        """,

        """
        CREATE TABLE IF NOT EXISTS bets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            probability DECIMAL(5, 4) NOT NULL,
            outcome VARCHAR(10) NOT NULL,
            stake_before DECIMAL(10, 2) NOT NULL,
            stake_after DECIMAL(10, 2) NOT NULL,
            strategy_used VARCHAR(50),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES betting_sessions(id) ON DELETE CASCADE
        ) ;
        """,

        """
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gambler_id INT NOT NULL,
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATETIME NULL,
            status VARCHAR(20) DEFAULT 'INITIALIZED',
            end_reason VARCHAR(50) NULL,
            initial_stake DECIMAL(10, 2),
            current_stake DECIMAL(10, 2),
            FOREIGN KEY (gambler_id) REFERENCES gambler(id) ON DELETE CASCADE
        ) ;
        """,
        """
        CREATE TABLE IF NOT EXISTS pause_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT NOT NULL,
            pause_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            resume_time DATETIME NULL,
            reason VARCHAR(255),
            FOREIGN KEY (session_id) REFERENCES game_sessions(id) ON DELETE CASCADE
        ) ;
        """,

        """
        CREATE TABLE IF NOT EXISTS game_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT NOT NULL,
            bet_amount DECIMAL(10, 2) NOT NULL,
            outcome VARCHAR(10) NOT NULL,
            stake_before DECIMAL(10, 2) NOT NULL,
            stake_after DECIMAL(10, 2) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES game_sessions(id) ON DELETE CASCADE
        ) ;
        """,
        """
        CREATE TABLE IF NOT EXISTS session_statistics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT NOT NULL,
            gambler_id INT NOT NULL,
            total_games INT DEFAULT 0,
            wins INT DEFAULT 0,
            losses INT DEFAULT 0,
            total_winnings DECIMAL(10, 2) DEFAULT 0.0,
            total_losses DECIMAL(10, 2) DEFAULT 0.0,
            net_profit DECIMAL(10, 2) DEFAULT 0.0,
            win_rate DECIMAL(5, 2) DEFAULT 0.0,
            longest_win_streak INT DEFAULT 0,
            longest_loss_streak INT DEFAULT 0,
            profit_factor DECIMAL(5, 2) DEFAULT 0.0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES game_sessions(id) ON DELETE CASCADE,
            FOREIGN KEY (gambler_id) REFERENCES gambler(id) ON DELETE CASCADE
        ) ;
        """,
        """
        CREATE TABLE IF NOT EXISTS stake_transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gambler_id INT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            amount DECIMAL(10, 2) NOT NULL,
            transaction_type VARCHAR(50) NOT NULL,
            balance_after DECIMAL(10, 2) NOT NULL,
            bet_id INT,
            FOREIGN KEY (gambler_id) REFERENCES gambler(id) ON DELETE CASCADE,
            FOREIGN KEY (bet_id) REFERENCES bets(id) ON DELETE SET NULL
        ) ;
        """
    ]

    for q in queries:
        cursor.execute(q)

    conn.commit()
    cursor.close()
    conn.close()

