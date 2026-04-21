from typing import Dict, Any

class GameStatusDisplay:
    @staticmethod
    def display_current_status(stake: float, status_msg: str = "ACTIVE"):
        print("\n" + "="*30)
        print(f" STATUS : Current Balance: Rs{stake:.2f}")
        print(f" ALERT : Boundary: {status_msg}")
        print("="*30)

    @staticmethod
    def display_game_outcome(outcome: str, winnings: float, updated_stake: float):
        print(f"\n >>> OUTCOME: {outcome}! <<<")
        print(f"     Payout:  ${winnings:.2f}")
        print(f"     Balance: ${updated_stake:.2f}")

class SessionSummary:
    @staticmethod
    def display_session_summary(stats: Dict[str, Any], title: str = "COMPREHENSIVE SESSION SUMMARY"):
        print(f"\n{'=' * 10} {title} {'=' * 10}")
        for key, value in stats.items():
            # Format floats to 2 decimal places for cleaner display
            if isinstance(value, float):
                print(f" * {key}: {value:.2f}")
            else:
                print(f" * {key}: {value}")
        print("=" * (22 + len(title)))