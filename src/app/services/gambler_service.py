from src.app.db.connection import get_connection

class GamblerService:

    # CREATE
    @staticmethod
    def create_gambler(gambler, preferences):
        if gambler.initial_stake <= 0:
            raise ValueError("Stake must be positive")

        if gambler.loss_threshold >= gambler.win_threshold:
            raise ValueError("Invalid thresholds")

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO gambler 
        (name, initial_stake, current_stake, win_threshold, loss_threshold,
         total_bets, wins, losses,
         max_bet, min_bet, game_type, auto_play, session_limit)
        VALUES (%s, %s, %s, %s, %s, 0, 0, 0, %s, %s, %s, %s, %s)
        """

        values = (
            gambler.name,
            gambler.initial_stake,
            gambler.current_stake,
            gambler.win_threshold,
            gambler.loss_threshold,
            preferences.max_bet,
            preferences.min_bet,
            preferences.game_type,
            preferences.auto_play,
            preferences.session_limit
        )

        cursor.execute(query, values)
        conn.commit()

        gambler_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return gambler_id

    # UPDATE
    @staticmethod
    def update_gambler(gambler_id, name=None, win_threshold=None, loss_threshold=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE gambler
        SET name = COALESCE(%s, name),
            win_threshold = COALESCE(%s, win_threshold),
            loss_threshold = COALESCE(%s, loss_threshold)
        WHERE id = %s
        """

        cursor.execute(query, (name, win_threshold, loss_threshold, gambler_id))
        conn.commit()

        cursor.close()
        conn.close()

    # RETRIEVE + STATISTICS
    @staticmethod
    def get_gambler(gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM gambler WHERE id = %s", (gambler_id,))
        data = cursor.fetchone()

        cursor.close()
        conn.close()

        return data

    # VALIDATE
    @staticmethod
    def validate_gambler(gambler):
        if gambler['current_stake'] <= 0:
            return False
        return True

    # RESET (proportional)
    @staticmethod
    def reset_gambler(gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM gambler WHERE id = %s", (gambler_id,))
        data = cursor.fetchone()

        ratio = data['win_threshold'] / data['initial_stake']

        new_win = data['initial_stake'] * ratio

        cursor.execute("""
        UPDATE gambler
        SET current_stake = initial_stake,
            total_bets = 0,
            wins = 0,
            losses = 0,
            win_threshold = %s
        WHERE id = %s
        """, (new_win, gambler_id))

        conn.commit()

        cursor.close()
        conn.close()