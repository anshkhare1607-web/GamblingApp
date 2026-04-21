from src.app.services.game_session_manager import GameSessionManager
from src.app.models.session_models import SessionParameters
from src.app.models.session_enums import SessionEndReason
from src.app.ui.game_displays import GameStatusDisplay, SessionSummary
from src.app.ui.interactive_menu import InteractiveMenu
from src.app.models.gambler import Gambler
from src.app.models.betting_preferences import BettingPreferences
from src.app.services.gambler_service import GamblerService


class SimpleGameEngine:
    def __init__(self):
        # Initialize UC07 UI Components
        self.menu = InteractiveMenu()
        self.display = GameStatusDisplay()
        self.summary = SessionSummary()
        
        # Initialize Backend Services
        self.session_manager = GameSessionManager()

    def run(self):
        while True:
            choice = self.menu.display_main_menu()
            if choice == "0":
                # 1. Get the details from the UI
                data = self.menu.prompt_for_gambler_details()
                
                # 2. Build the Models
                gambler = Gambler(data["name"], data["stake"], data["win"], data["loss"])
                pref = BettingPreferences(data["max_bet"], data["min_bet"], data["game_type"], auto_play=False, session_limit=60)
                
                # 3. Save to Database
                try:
                    gid = GamblerService.create_gambler(gambler, pref)
                    print(f"\n Gambler Profile Created Successfully Your ID is: {gid}")
                    print("    (Remember this ID to start your session)")
                except Exception as e:
                    print(f"\nError creating gambler: {e}")
                          
            if choice == "1":
                g_id = self.menu.prompt_for_id()
                # For demo purposes, hardcoding initial parameters
                params = SessionParameters(upper_limit=2000, lower_limit=200, min_bet=10, max_bet=500, max_games=50, max_duration_sec=3600)
                try:
                    sess = self.session_manager.start_new_session(g_id, 1000.0, params)
                    print(f"\nSession {sess.session_id} Started Successfully!")
                    self.display.display_current_status(sess.current_stake, sess.status.value)
                except Exception as e:
                    print(f"Error: {e}")

            elif choice == "2":
                g_id = self.menu.prompt_for_id()
                sess = self.session_manager.get_session(g_id)
                
                if not sess or sess.status.value != "ACTIVE":
                    print("No active session found. Start one first.")
                    continue
                
                # UC07: Prompt for bet
                bet_amount = self.menu.prompt_for_bet_amount(sess.current_stake)
                
                stake_before = sess.current_stake
                result_msg = sess.play_game(bet_amount)
                
                # Determine outcome context for display
                outcome = "WIN" if sess.current_stake > stake_before else "LOSS"
                winnings = (sess.current_stake - stake_before) + bet_amount if outcome == "WIN" else 0.0
                
                #Display outcome and updated status
                self.display.display_game_outcome(outcome, winnings, sess.current_stake)
                
                # If the game caused the session to auto-end due to limits
                if sess.status.value != "ACTIVE":
                    print(f"\nSESSION AUTO-ENDED: {sess.end_reason.value}")
                    self.summary.display_session_summary(sess.get_statistics(), "FINAL REPORT")

            elif choice == "3":
                g_id = self.menu.prompt_for_id()
                sess = self.session_manager.get_session(g_id)
                if sess:
                    self.display.display_current_status(sess.current_stake, sess.status.value)
                else:
                    print("Session not found.")

            elif choice == "4":
                g_id = self.menu.prompt_for_id()
                sess = self.session_manager.get_session(g_id)
                if sess:
                    if sess.status.value == "ACTIVE":
                        sess.end_session(SessionEndReason.MANUAL)
                    self.summary.display_session_summary(sess.get_statistics(), "FINAL REPORT")
                else:
                    print("Session not found.")

            elif choice == "5":
                print("Shutting down")
                break