from src.app.db.connection import get_connection

def create_betting_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    session_query = """
    CREATE TABLE IF NOT EXISTS betting_sessions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gambler_id INT NOT NULL,
        start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        end_time DATETIME NULL,
        status VARCHAR(20) DEFAULT 'ACTIVE',
        FOREIGN KEY (gambler_id) REFERENCES gambler(id) ON DELETE CASCADE
    )
    """
    
    bet_query = """
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
    )
    """
    
    cursor.execute(session_query)
    cursor.execute(bet_query)
    conn.commit()
    
    cursor.close()
    conn.close()
    print("Tables 'betting_sessions' and 'bets' created successfully.")

if __name__ == "__main__":
    create_betting_tables()