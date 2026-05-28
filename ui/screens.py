import time
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.rule import Rule

from ui.console import *
from ui.components import *

#  MENU -----------------

def show_main_menu() -> str:
    """
    Render the main menu and return the player's choice.
    """

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", width=3)
    table.add_column()
    table.add_row("1", "[green]New Run[/green]")
    table.add_row("2", "[cyan]Run Records[/cyan]")
    table.add_row("3", "[red]Quit[/red]")
 
    console.print()
    console.print(Panel(
        table,
        title="[bold yellow]🔱  H A D E S -1 —  Underworld Roguelite  🔱[/]",
        border_style="yellow",
        padding=(1, 4),
    ))
    return ask("  Choice", ["1", "2", "3"])

# run prep ----------

def prompt_nickname() -> str:
    """Ask for a nickname, reject empty strings."""
    while True:
        nick = Prompt.ask("\n  [bold cyan]Enter your nickname[/bold cyan]",
                          console=console).strip()
        if nick:
            return nick
        console.print("  [red]Nickname cannot be empty.[/red]")
 
 
def show_run_intro(player: "Player") -> None:  # type: ignore[name-defined]
    console.print()
    console.print(Panel(
        "[bold]A new attempt to escape the Underworld begins.[/bold]\n"
        "[dim]Power, strategy, and divine favour will determine your fate.[/dim]",
        title="[bold yellow]⚔️   N E W   R U N   ⚔️[/bold yellow]",
        border_style="yellow",
        padding=(1, 4),
    ))
    console.print(
        f"\n  Welcome, [bold cyan]{player.name}[/bold cyan]!  "
        f"Starting power: [green]{player.power}[/green]  ·  "
        f"HP: [green]{player.hp}[/green]"
    )
    pause(0.4)
 
 
def show_starting_boon(boon: "Boon") -> None:  # type: ignore[name-defined]
    console.print()
    console.print(Panel(
        boon_as_text(boon),
        title="[bold yellow]🌟  A Boon appears at the start of your journey![/bold yellow]",
        subtitle=f"[cyan]{boon.god} reaches out to you in the depths...[/cyan]",
        border_style="yellow",
        padding=(1, 4),
    ))
 
 
def show_legendary_unlock() -> None:
    console.print("  [bold yellow]✨  Legendary Boon! Special Attack unlocked![/bold yellow]")

# Entering an new room -----

def show_room_intro(room: int, enemies: list, is_boss: bool) -> None:
    console.print()
    if is_boss:
        console.print(Panel(
            f"[bold]A terrifying boss awaits...[/bold]\n"
            f"[dim]Power: {enemies[0].power}  ·  HP: {enemies[0].hp}[/dim]",
            title=f"[bold red]💀  BOSS ROOM — Room {room}  💀[/bold red]",
            border_style="red",
            padding=(1, 4),
        ))
    else:
        console.print(Panel(
            f"[bold]{len(enemies)} enemy/enemies emerge from the shadows![/bold]",
            title=f"[bold yellow]⚔️   Room {room}[/bold yellow]",
            border_style="yellow",
            padding=(0, 2),
        ))
    pause(0.6)
 
 
def show_enemy_intro(enemy: "Enemy", idX: int, total: int) -> None:  # type: ignore[name-defined]
    console.print()
    console.print(Panel(
        f"  [bold]Power:[/bold] {enemy.power}   "
        f"[bold]HP:[/bold] {enemy.hp}/{enemy.max_hp}",
        title=f"[bold red]Enemy {idX}/{total}: {enemy.name}[/bold red]",
        border_style="red",
    ))
    pause(0.3)
 
 # ----------------- Combat round ---------------------------------------------
 
def show_round_status(player: "Player", enemy: "Enemy",  # type: ignore[name-defined]
                      round_n: int, idx: int, total: int) -> None:
    console.print()
    console.print(status_panel(player, enemy, round_n, idx, total))
 
 
def show_action_menu(player: "Player") -> str:  # type: ignore[name-defined]
    """Render the action table and return the player's validated choice."""
    table, options = action_table(player)
    console.print(Panel(table, title="[bold]Actions[/bold]",
                        border_style="bright_black", padding=(0, 1)))
    return ask("  Action", options)
 
 
# ------------------------- Combat results ------------------------------------
 
def show_player_attack(enemy_name: str, damage: int) -> None:
    console.print(f"\n  ⚔️  [green]You hit [bold]{enemy_name}[/bold] for [bold]{damage}[/bold] damage![/green]")
 
def show_player_special(damage: int) -> None:
    console.print(f"\n  [bold yellow]✨  SPECIAL ATTACK! [white]{damage}[/white] devastating damage![/bold yellow]")
 
def show_special_error(error: str) -> None:
    console.print(f"\n  [red]❌  {error}[/red]")
 
def show_dodge_stance() -> None:
    console.print("\n  💨 [cyan]You brace to dodge...[/cyan]")
 
def show_defend_stance() -> None:
    console.print("\n  🛡️  [cyan]You raise your guard![/cyan]")
 
def show_dodge_success(enemy_name: str, damage_avoided: int) -> None:
    console.print(f"  💨 [green]Dodged! Avoided [bold]{damage_avoided}[/bold] damage from {enemy_name}.[/green]")
 
def show_dodge_fail(enemy_name: str, damage: int) -> None:
    console.print(f"  😰 [yellow]Dodge failed! {enemy_name} hit you for [bold]{damage}[/bold].[/yellow]")
 
def show_block_result(enemy_name: str, raw: int, taken: int) -> None:
    console.print(f"  🛡️  [yellow]{enemy_name} struck for {raw} → blocked half → took [bold]{taken}[/bold].[/yellow]")
 
def show_direct_hit(enemy_name: str, damage: int) -> None:
    console.print(f"  💥 [bold red]{enemy_name} hit you for [bold]{damage}[/bold] damage![/bold red]")
 
def show_enemy_defeated(enemy_name: str) -> None:
    console.print(f"\n  ✅  [bold green]{enemy_name} defeated![/bold green]")
    pause(0.4)
 
def show_player_death(player_name: str, enemy_name: str) -> None:
    console.print()
    console.print(Panel(
        f"[dim]{player_name} falls before reaching the surface...[/dim]",
        title=f"[bold red]💀  Slain by {enemy_name}[/bold red]",
        border_style="red",
        padding=(1, 4),
    ))
 
def show_room_cleared(room: int) -> None:
    console.print(f"\n  [bold green]🎉  Room {room} cleared![/bold green]")
 
 
# ------------- Boon offer ---------------------------------------------------------------
 
def show_boon_offer(god: str, boons: list, room: int) -> str:
    """Render the boon selection table and return '1', '2', '3', or '4'."""
    console.print()
    console.print(Panel(
        boon_choice_table(boons),
        title=f"[bold yellow]🌟  {god} offers a blessing — Room {room}  🌟[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
    ))
    return ask("  Choose a boon", ["1", "2", "3", "4"])
 
def show_boon_acquired(boon: "Boon", new_power: int) -> None:  # type: ignore[name-defined]
    console.print(f"\n  ✅  [green]Boon acquired![/green]  {boon_as_text(boon)}")
    console.print(f"  Power is now: [bold green]{new_power}[/bold green]")
 
def show_boon_declined() -> None:
    console.print("\n  [dim]You declined the gods' gifts...[/dim]")
 
 
# ----------------- End of room ------------------
 
def show_room_summary(player: "Player", room: int) -> None:  # type: ignore[name-defined]
    grid = Table.grid(padding=(0, 3))
    grid.add_column()
    grid.add_column()
    grid.add_column()
    grid.add_row(
        f"[bold]Room {room} complete[/bold]",
        f"Power: [bold green]{player.power}[/bold green]",
        f"HP: {hp_bar(player.hp, player.max_hp)}",
    )
    console.print()
    console.print(Panel(grid, border_style="green", padding=(0, 2)))
 
 
def show_continue_prompt(next_room: int) -> str:
    """Returns '1' (advance) or '2' (retreat)."""
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", width=3)
    table.add_column()
    table.add_row("1", f"[green]Advance to Room {next_room}[/green]")
    table.add_row("2", "[cyan]Retreat (give up this run)[/cyan]")
    console.print(Panel(table, border_style="bright_black", padding=(0, 2)))
    return ask("  Choice", ["1", "2"])
 
 
# ── Run end -----------------------
 
def show_run_over(player_name: str, rooms_cleared: int, final_power: int) -> None:
    console.print(Panel(
        f"Rooms cleared: [bold]{rooms_cleared}[/bold]  ·  "
        f"Final power: [bold]{final_power}[/bold]",
        title="[bold red]Run Over[/bold red]",
        border_style="red",
        padding=(1, 4),
    ))
 
def show_retreat(player_name: str) -> None:
    console.print(f"\n  [cyan]{player_name} retreats to the Underworld with honour...[/cyan]")
 
 
#  Leaderboard --------------
 
def show_leaderboard(records: list[dict]) -> None:
    console.print()
    if not records:
        console.print(Panel(
            "[dim]No runs recorded yet. Be the first![/dim]",
            title="[bold yellow]🏆  Run Records  🏆[/bold yellow]",
            border_style="yellow",
            padding=(1, 4),
        ))
    else:
        console.print(Panel(
            leaderboard_table(records),
            title="[bold yellow]🏆  Run Records  🏆[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        ))
    time.sleep(1.5)
 