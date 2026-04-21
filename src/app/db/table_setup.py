from src.app.db.connection import get_connection

def create_transactions_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    CREATE TABLE IF NOT EXISTS stake_transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gambler_id INT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        amount DECIMAL(10, 2) NOT NULL,
        transaction_type VARCHAR(50) NOT NULL,
        balance_after DECIMAL(10, 2) NOT NULL,
        bet_id VARCHAR(50),
        FOREIGN KEY (gambler_id) REFERENCES gambler(id) ON DELETE CASCADE
    )
    """
    cursor.execute(query)
    conn.commit()
    
    cursor.close()
    conn.close()
    print("Table 'stake_transactions' created successfully.")

if __name__ == "__main__":
    create_transactions_table()