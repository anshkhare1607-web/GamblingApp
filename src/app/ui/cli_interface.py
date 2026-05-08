from typing import Dict, Any
from src.app.services.input_validator import InputValidator
from src.app.exceptions.validation_exceptions import ValidationException

class SafeInputHandler:
    def __init__(self):
        self.validator = InputValidator()
        
    def get_valid_numeric(self, prompt: str) -> float:
        while True:
            user_input = input(prompt)
            try:
                val = self.validator.parse_and_validate_numeric(user_input, "Input")
                return val
            except ValidationException as e:
                print(f"{e.error_type.value}: {e}")

class CLIInterface:
    def __init__(self):
        self.input_handler = SafeInputHandler()
        
    def display_main_menu(self) -> str:
        print("\n--- GAMBLING APP: ---")
        print("0. Create New Gambler Profile") 
        print("1. Start Managed Session")
        print("2. Play Next Game")
        print("3. View Real-Time Status")
        print("4. End Session & View Summary")
        print("5. Pause / Resume Session")  
        print("6. Exit")                    
        return input("Select an operation: ")
        
    def prompt_for_gambler_details(self) -> dict:
        print("\n--- CREATE NEW GAMBLER ---")
        name = input("Name: ")
        stake = self.input_handler.get_valid_numeric("Initial Stake: ")
        win = self.input_handler.get_valid_numeric("Win Threshold: ")
        loss = self.input_handler.get_valid_numeric("Loss Threshold (Can be 0): ")
        max_bet = self.input_handler.get_valid_numeric("Max Bet: ")
        min_bet = self.input_handler.get_valid_numeric("Min Bet: ")
        game_type = input("Preferred Game Type (e.g., Slots, Blackjack): ")
        
        return {
            "name": name, "stake": stake, "win": win, "loss": loss,
            "max_bet": max_bet, "min_bet": min_bet, "game_type": game_type
        }
        
    @staticmethod
    def display_current_status(stake: float, status_msg: str = "ACTIVE"):
        print("\n" + "="*30)
        print(f" STATUS : Current Balance: Rs{stake:.2f}")
        print(f" ALERT  : Boundary: {status_msg}")
        print("="*30)
        
    @staticmethod
    def display_session_summary(stats: Dict[str, Any], title: str = "SESSION SUMMARY"):
        print(f"\n{'=' * 10} {title} {'=' * 10}")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f" * {key}: {value:.2f}")
            else:
                print(f" * {key}: {value}")
        print("=" * (22 + len(title)))
        
    @staticmethod
    def display_game_outcome(outcome: str, winnings: float, updated_stake: float):
        print(f"\n >>> OUTCOME: {outcome}! <<<")
        print(f"     Payout:  ${winnings:.2f}")
        print(f"     Balance: ${updated_stake:.2f}")