import random
from datetime import datetime
from typing import Dict, Optional
from src.app.db.connection import get_connection
from src.app.models.session_enums import SessionStatus, SessionEndReason
from src.app.models.session_models import SessionParameters, PauseRecord, GameRecord

class GamingSession:
    def __init__(self, session_id: int, gambler_id: int, initial_stake: float, params: SessionParameters):
        self.session_id = session_id
        self.gambler_id = gambler_id
        self.current_stake = initial_stake
        self.params = params
        self.status = SessionStatus.INITIALIZED
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.end_reason: Optional[SessionEndReason] = None
        
        self.games = []
        self.pauses = []
        self.current_pause: Optional[PauseRecord] = None

    def start(self):
        self.status = SessionStatus.ACTIVE
        self._update_db_status()

    def pause(self, reason: str):
        if self.status == SessionStatus.ACTIVE:
            self.status = SessionStatus.PAUSED
            self.current_pause = PauseRecord(reason)
            self.pauses.append(self.current_pause)
            self._update_db_status()

    def resume(self):
        if self.status == SessionStatus.PAUSED and self.current_pause:
            self.current_pause.resume()
            self.status = SessionStatus.ACTIVE
            self.current_pause = None
            self._update_db_status()

    def play_game(self, bet_amount: float) -> str:
        if self.status != SessionStatus.ACTIVE:
            return f"Cannot play: Session is {self.status.value}"
        
        if not (self.params.min_bet <= bet_amount <= self.params.max_bet):
            return "Bet amount out of bounds."
            
        if bet_amount > self.current_stake:
            return "Insufficient stake."

        # Check timeouts and game limits before playing
        if len(self.games) >= self.params.max_games:
            self.end_session(SessionEndReason.MAX_GAMES)
            return "Session ended: Max games reached."

        stake_before = self.current_stake
        is_win = random.random() <= self.params.default_prob
        
        if is_win:
            win_amount = bet_amount * 2  # Simplified 1:1 payout
            self.current_stake += (win_amount - bet_amount)
            outcome = "WIN"
        else:
            self.current_stake -= bet_amount
            outcome = "LOSS"

        record = GameRecord(bet_amount, outcome, stake_before, self.current_stake)
        self.games.append(record)
        
        # Save game to DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO game_records (session_id, bet_amount, outcome, stake_before, stake_after) VALUES (%s, %s, %s, %s, %s)",
            (self.session_id, bet_amount, outcome, stake_before, self.current_stake)
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Check boundaries immediately after game
        self._check_boundaries()
        return f"Result: {outcome}. New Balance: {self.current_stake:.2f}"

    def _check_boundaries(self):
        if self.current_stake >= self.params.upper_limit:
            self.end_session(SessionEndReason.UPPER_LIMIT)
        elif self.current_stake <= self.params.lower_limit:
            self.end_session(SessionEndReason.LOWER_LIMIT)

    def end_session(self, reason: SessionEndReason):
        if self.status in [SessionStatus.ENDED_WIN, SessionStatus.ENDED_LOSS, SessionStatus.ENDED_MANUAL, SessionStatus.ENDED_TIMEOUT]:
            return

        self.end_time = datetime.now()
        self.end_reason = reason
        
        if reason == SessionEndReason.UPPER_LIMIT:
            self.status = SessionStatus.ENDED_WIN
        elif reason == SessionEndReason.LOWER_LIMIT:
            self.status = SessionStatus.ENDED_LOSS
        elif reason == SessionEndReason.TIMEOUT:
            self.status = SessionStatus.ENDED_TIMEOUT
        else:
            self.status = SessionStatus.ENDED_MANUAL

        self._update_db_status()

    def _update_db_status(self):
        conn = get_connection()
        cursor = conn.cursor()
        reason_val = self.end_reason.value if self.end_reason else None
        cursor.execute(
            "UPDATE game_sessions SET status = %s, current_stake = %s, end_time = %s, end_reason = %s WHERE id = %s",
            (self.status.value, self.current_stake, self.end_time, reason_val, self.session_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_statistics(self):
        total_time = (datetime.now() - self.start_time).total_seconds() if not self.end_time else (self.end_time - self.start_time).total_seconds()
        paused_time = sum(p.get_duration_sec() for p in self.pauses)
        active_time = total_time - paused_time
        wins = sum(1 for g in self.games if g.outcome == "WIN")
        
        return {
            "Total Duration (s)": round(total_time, 2),
            "Active Play (s)": round(active_time, 2),
            "Paused Duration (s)": round(paused_time, 2),
            "Games Played": len(self.games),
            "Win Rate (%)": round((wins / len(self.games) * 100) if self.games else 0, 2),
            "Status": self.status.value,
            "End Reason": self.end_reason.value if self.end_reason else "N/A"
        }

class GameSessionManager:
    def __init__(self):
        self.active_sessions: Dict[int, GamingSession] = {} # gambler_id -> session

    def start_new_session(self, gambler_id: int, initial_stake: float, params: SessionParameters) -> GamingSession:
        if gambler_id in self.active_sessions and self.active_sessions[gambler_id].status in [SessionStatus.ACTIVE, SessionStatus.PAUSED]:
            raise ValueError("Gambler already has an active session.")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO game_sessions (gambler_id, initial_stake, current_stake) VALUES (%s, %s, %s)",
            (gambler_id, initial_stake, initial_stake)
        )
        conn.commit()
        session_id = cursor.lastrowid
        cursor.close()
        conn.close()

        session = GamingSession(session_id, gambler_id, initial_stake, params)
        session.start()
        self.active_sessions[gambler_id] = session
        return session

    def get_session(self, gambler_id: int) -> Optional[GamingSession]:
        return self.active_sessions.get(gambler_id)