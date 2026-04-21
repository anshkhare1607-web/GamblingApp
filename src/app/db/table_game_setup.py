from src.app.db.connection import get_connection

def create_game_session_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    session_query = """
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
    )
    """
    
    pause_query = """
    CREATE TABLE IF NOT EXISTS pause_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id INT NOT NULL,
        pause_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        resume_time DATETIME NULL,
        reason VARCHAR(255),
        FOREIGN KEY (session_id) REFERENCES game_sessions(id) ON DELETE CASCADE
    )
    """
    
    game_query = """
    CREATE TABLE IF NOT EXISTS game_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id INT NOT NULL,
        bet_amount DECIMAL(10, 2) NOT NULL,
        outcome VARCHAR(10) NOT NULL,
        stake_before DECIMAL(10, 2) NOT NULL,
        stake_after DECIMAL(10, 2) NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES game_sessions(id) ON DELETE CASCADE
    )
    """
    
    cursor.execute(session_query)
    cursor.execute(pause_query)
    cursor.execute(game_query)
    conn.commit()
    
    cursor.close()
    conn.close()
    print("Tables 'game_sessions', 'pause_records', and 'game_records' created successfully.")

if __name__ == "__main__":
    create_game_session_tables()