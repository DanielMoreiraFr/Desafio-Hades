import time
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def ask(prompt_text: str, valid: list[str]) -> str:
    """
    Prompt until the player enter one of the valid choices from the options list.
    """
    while True:
        choice = Prompt.ask(prompt_text, console=console).strip()

        if choice in valid:
            return choice
        console.print(f"  [red]❌  Invalid option.[/red]  Choose from: {', '.join(valid)}")

def wait(message: str = "[ENTER to continue]") -> None:
    Prompt.ask(f"\n  [dim]{message}[/dim]", default="", console=console)
 
 
def pause(seconds: float = 0.5) -> None:
    time.sleep(seconds)