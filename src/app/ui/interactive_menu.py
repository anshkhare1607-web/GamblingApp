from src.app.ui.safe_input_handler import SafeInputHandler

class InteractiveMenu:
    def __init__(self):
        self.input_handler = SafeInputHandler()

    def prompt_for_bet_amount(self, current_stake: float) -> float:
        print("\n--- PLACE YOUR BET ---")
        return self.input_handler.get_valid_bet(f"Enter Bet Amount (Max Rs{current_stake:.2f}): ", current_stake)
    
    def prompt_for_id(self, prompt: str = "Enter Gambler ID : ") -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid ID. Must be an integer")
    
    def display_main_menu(self) -> str:
        print("\n--- GAMBLING APP: ---")
        print("0. Create New Gambler Profile") 
        print("1. Start Managed Session")
        print("2. Play Next Game")
        print("3. View Real-Time Status")
        print("4. End Session & View Summary")
        print("5. Exit")
        return input("Select an operation: ")

    def prompt_for_gambler_details(self) -> dict:
        print("\n--- CREATE NEW GAMBLER ---")
        name = input("Name: ")
        
        #Validation
        stake = self.input_handler.get_valid_stake("Initial Stake: ")
        win = self.input_handler.get_valid_stake("Win Threshold: ")
        loss = self.input_handler.get_valid_stake("Loss Threshold (Can be 0): ")
        max_bet = self.input_handler.get_valid_stake("Max Bet: ")
        min_bet = self.input_handler.get_valid_stake("Min Bet: ")
        
        game_type = input("Preferred Game Type (e.g., Slots, Blackjack): ")
        
        return {
            "name": name, "stake": stake, "win": win, "loss": loss,
            "max_bet": max_bet, "min_bet": min_bet, "game_type": game_type
        }