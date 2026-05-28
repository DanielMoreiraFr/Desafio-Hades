from run import start_run
from systems.records import load_records
from ui.screens import show_main_menu, show_leaderboard

 
 
def main() -> None:
    while True:
        choice = show_main_menu()
 
        if choice == "1":
            start_run()
        elif choice == "2":
            show_leaderboard(load_records())
        elif choice == "3":
            from ui.console import console
            console.print("\n  [cyan]Farewell, son of Hades. ⚔️[/cyan]\n")
            break
 
 
if __name__ == "__main__":
    main()
 