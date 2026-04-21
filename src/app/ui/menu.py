from src.app.models.gambler import Gambler
from src.app.models.betting_preferences import BettingPreferences
from src.app.services.gambler_service import GamblerService
from src.app.models.statistics import GamblerStatistics
from src.app.services.stake_management_service import StakeManagementService

current_stake_service = None

def menu():
    global current_stake_service
    while True:
        print("\n--- GAMBLING APP MENU ---")
        print("1. Create Gambler")
        print("2. Update Gambler")
        print("3. View Stats")
        print("4. Reset Gambler")
        print("5. Init Stake Session")
        print("6. Place Bet")
        print("7. Process Outcome")
        print("8. View Stake Report")
        print("9. Exit")

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
            print("Gambler updated.")

        elif choice == "3":
            gid = int(input("ID: "))
            data = GamblerService.get_gambler(gid)
            if data:
                stats = GamblerStatistics(data)
                print("\n--- STATS ---")
                print("Name:", stats.name)
                print("Stake:", stats.current_stake)
                print("Win Rate:", stats.win_rate(), "%")
                print("Profit:", stats.net_profit())
                print("Status:", stats.threshold_status(data['win_threshold'], data['loss_threshold']))
            else:
                print("Gambler not found.")

        elif choice == "4":
            gid = int(input("ID: "))
            GamblerService.reset_gambler(gid)
            print("Reset done")

        elif choice == "5":
            g_id = int(input("Gambler ID: "))
            stake = float(input("Initial Stake: "))
            min_limit = float(input("Lower Limit (e.g. 100): "))
            max_limit = float(input("Upper Limit (e.g. 2000): "))
            try:
                current_stake_service = StakeManagementService(g_id, stake, min_limit, max_limit)
                print("Stake management session initialized.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "6":
            if not current_stake_service:
                print("Initialize stake session (Option 5) first!")
                continue
            amt = float(input("Bet Amount: "))
            b_id = input("Bet ID: ")
            status = current_stake_service.process_bet_placed(amt, b_id)
            print(f"Bet placed. Current Balance: {current_stake_service.monitor.current_stake}. Status: {status}")

        elif choice == "7":
            if not current_stake_service:
                print("Initialize stake session (Option 5) first!")
                continue
            # If the user lost the bet, they win 0. If they won, input the payout amount.
            amt = float(input("Amount Won (Enter 0 if loss): "))
            b_id = input("Bet ID: ")
            status = current_stake_service.process_bet_outcome(amt, b_id)
            print(f"Outcome processed. Current Balance: {current_stake_service.monitor.current_stake}. Status: {status}")

        elif choice == "8":
            if not current_stake_service:
                print("Initialize stake session (Option 5) first!")
                continue
            report = current_stake_service.generate_report()
            print("\n--- STAKE REPORT ---")
            print(f"Initial Balance: {report.initial_balance}")
            print(f"Net Profit: {report.calculate_net_profit()}")
            print(f"Volatility (Avg Change): {current_stake_service.monitor.calculate_volatility():.2f}")
            print(f"Peak Stake: {current_stake_service.monitor.peak_stake}")
            print(f"Lowest Stake: {current_stake_service.monitor.lowest_stake}")
            print("Transactions:")
            for t in report.transactions:
                print(f"  [{t.timestamp.strftime('%H:%M:%S')}] {t.transaction_type.value} | Amt: {t.amount} | Bal: {t.balance_after} | ID: {t.bet_id}")

        elif choice == "9":
            print("Exiting...")
            break

if __name__ == "__main__":
    menu()