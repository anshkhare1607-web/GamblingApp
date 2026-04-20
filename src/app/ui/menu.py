from src.app.models.gambler import Gambler
from src.app.models.betting_preferences import BettingPreferences
from src.app.services.gambler_service import GamblerService
from src.app.models.statistics import GamblerStatistics


def menu():
    while True:
        print("\n1. Create Gambler")
        print("2. Update Gambler")
        print("3. View Stats")
        print("4. Reset Gambler")
        print("5. Exit")

        choice = input("Choice: ")

        if choice == "1":
            name = input("Name: ")
            stake = float(input("Stake: "))
            win = float(input("Win Threshold: "))
            loss = float(input("Loss Threshold: "))

            max_bet = float(input("Max Bet: "))
            min_bet = float(input("Min Bet: "))
            game_type = input("Game Type: ")
            auto = input("Auto Play (true/false): ") == "true"
            session = int(input("Session Limit: "))

            gambler = Gambler(name, stake, win, loss)
            pref = BettingPreferences(max_bet, min_bet, game_type, auto, session)

            gid = GamblerService.create_gambler(gambler, pref)
            print("Created ID:", gid)

        elif choice == "2":
            gid = int(input("ID: "))
            name = input("New Name: ")
            GamblerService.update_gambler(gid, name=name)

        elif choice == "3":
            gid = int(input("ID: "))
            data = GamblerService.get_gambler(gid)

            stats = GamblerStatistics(data)

            print("\n--- STATS ---")
            print("Name:", stats.name)
            print("Stake:", stats.current_stake)
            print("Win Rate:", stats.win_rate())
            print("Profit:", stats.net_profit())
            print("Status:", stats.threshold_status(data['win_threshold'], data['loss_threshold']))

        elif choice == "4":
            gid = int(input("ID: "))
            GamblerService.reset_gambler(gid)
            print("Reset done")

        elif choice == "5":
            break