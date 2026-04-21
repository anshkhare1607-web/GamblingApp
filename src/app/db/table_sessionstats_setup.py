from src.app.db.connection import get_connection

def create_statistics_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    stats_query = """
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
    )
    """
    
    cursor.execute(stats_query)
    conn.commit()
    
    cursor.close()
    conn.close()
    print("Table 'session_statistics' created successfully.")

if __name__ == "__main__":
    create_statistics_tables()