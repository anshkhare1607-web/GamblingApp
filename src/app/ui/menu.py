from src.app.models.gambler import Gambler
from src.app.models.betting_preferences import BettingPreferences
from src.app.services.gambler_service import GamblerService
from src.app.models.statistics import GamblerStatistics
from src.app.services.stake_management_service import StakeManagementService

from src.app.services.betting_service import BettingService
from src.app.models.strategy import (
    FixedAmountStrategy, 
    PercentageStrategy, 
    MartingaleStrategy, 
    ReverseMartingaleStrategy, 
    FibonacciStrategy, 
    DAlembertStrategy
)

from src.app.services.game_session_manager import GameSessionManager
from src.app.models.session_models import SessionParameters
from src.app.models.session_enums import SessionEndReason

current_betting_service = None
current_stake_service = None
current_betting_service = None
session_manager = GameSessionManager()

def menu():
    global current_stake_service
    global current_betting_service
    global session_manager
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
        print("9. Start Betting Session")
        print("10. Place Manual Bet")
        print("11. Run Strategy Simulation")
        print("12. Start Managed Session")
        print("13. Play Game")
        print("14. Pause Session")
        print("15. Resume Session")
        print("16. End Session Manually")
        print("17. View Session Stats")
        print("18. Exit")

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
            print("Gambler updated")

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
            min_limit = float(input("Lower Limit : "))
            max_limit = float(input("Upper Limit : "))
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
                print("Initialize stake session (Option 5) first")
                continue
            # If the user lost the bet, they win 0. If they won, input the payout amount.
            amt = float(input("Amount Won (Enter 0 if loss) : "))
            b_id = input("Bet ID: ")
            status = current_stake_service.process_bet_outcome(amt, b_id)
            print(f"Outcome processed. Current Balance : {current_stake_service.monitor.current_stake}. Status: {status}")

        elif choice == "8":
            if not current_stake_service:
                print("Initialize stake session (Option 5) first")
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
            if not current_stake_service:
                print("Initialize stake session (Option 5) first")
                continue
            current_betting_service = BettingService(current_stake_service)
            sid = current_betting_service.start_session()
            print(f"Betting Session {sid} started.")

        elif choice == "10":
            if not current_betting_service:
                print("Start Betting Session (Option 9) first")
                continue
            try:
                amt = float(input("Bet Amount: "))
                prob = float(input("Win Probability (0.01 to 1.00): "))
                outcome, win_amt, status = current_betting_service.place_bet(amt, prob)
                print(f"Outcome: {outcome}! Won: {win_amt:.2f}. Balance: {current_stake_service.monitor.current_stake}. Status: {status}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "11":
            if not current_betting_service:
                print("Start Betting Session (Option 9) first!")
                continue
            
            base = float(input("Base Bet Amount : "))
            prob = float(input("Win Probability (e.g., 0.45) : "))
            runs = int(input("Number of Consecutive Bets : "))
            
            print("\n--- STRATEGIES ---")
            print("1. Fixed Amount")
            print("2. Percentage (5%)")
            print("3. Martingale")
            print("4. Reverse Martingale")
            print("5. Fibonacci")
            print("6. D'Alembert")
            s_choice = input("Select Strategy: ")
            
            if s_choice == "1":
                strat = FixedAmountStrategy()
            elif s_choice == "2":
                strat = PercentageStrategy(5.0)
            elif s_choice == "3":
                strat = MartingaleStrategy()
            elif s_choice == "4":
                strat = ReverseMartingaleStrategy()
            elif s_choice == "5":
                strat = FibonacciStrategy()
            elif s_choice == "6":
                increment = float(input("Enter increment amount: "))
                strat = DAlembertStrategy(increment)
            else:
                print("Invalid strategy.")
                continue

            results = current_betting_service.place_consecutive_bets(runs, base, prob, strat)
            print("\n--- SIMULATION RESULTS ---")
            for r in results:
                print(r)

        elif choice == "12":
            g_id = int(input("Gambler ID: "))
            stake = float(input("Initial Stake: "))
            up_limit = float(input("Upper Win Limit: "))
            low_limit = float(input("Lower Loss Limit: "))
            
            params = SessionParameters(
                upper_limit=up_limit, 
                lower_limit=low_limit, 
                min_bet=10, 
                max_bet=500, 
                max_games=100, 
                max_duration_sec=3600
            )
            try:
                sess = session_manager.start_new_session(g_id, stake, params)
                print(f"Session {sess.session_id} started successfully!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "13":
            g_id = int(input("Gambler ID: "))
            sess = session_manager.get_session(g_id)
            if not sess:
                print("No active session found.")
                continue
            amt = float(input("Bet Amount: "))
            res = sess.play_game(amt)
            print(res)

        elif choice == "14":
            g_id = int(input("Gambler ID: "))
            sess = session_manager.get_session(g_id)
            if sess:
                reason = input("Pause Reason: ")
                sess.pause(reason)
                print("Session Paused.")

        elif choice == "15":
            g_id = int(input("Gambler ID: "))
            sess = session_manager.get_session(g_id)
            if sess:
                sess.resume()
                print("Session Resumed.")

        elif choice == "16":
            g_id = int(input("Gambler ID: "))
            sess = session_manager.get_session(g_id)
            if sess:
                sess.end_session(SessionEndReason.MANUAL)
                print("Session Ended Manually.")

        elif choice == "17":
            g_id = int(input("Gambler ID: "))
            sess = session_manager.get_session(g_id)
            if sess:
                stats = sess.get_statistics()
                print("\n--- SESSION STATS ---")
                for k, v in stats.items():
                    print(f"{k}: {v}")

        elif choice == "18":
            print("Exiting...")
            break

if __name__ == "__main__":
    menu()