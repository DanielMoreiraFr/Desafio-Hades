from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from CONFIG import RARITY_STYLE, RARITY_ICON, RARITY_POWER

# HP BAR --------------------------------------------------

def hp_bar(current: int, maximum: int, width: int = 20) -> Text:
    """Generates a Text object representing the HP bar, with color based on the percentage of HP remaining.
    
    Args:
        current (int): The current HP of the character.
        maximum (int): The maximum HP of the character.
        width (int, optional): The total width of the HP bar. Defaults to 20.
    
    Returns:
        Text: A Text object representing the HP bar."""
    
    ratio = max(0.0), min(1.0, current / maximum) if maximum > 0 else 0.0
    filled_length = int(width * ratio)
    bar = "█" * filled_length + "░" * (width - filled_length)
    if ratio > 0.5:
        color = 'green'
    elif ratio > 0.25:
        color = 'yellow'
    else:
        color = 'bold red'

    text = Text()
    text.append(f'[{bar}]', style=color)
    text.append(f'{current}/{maximum}', style= 'dim')
    return text

#  combat situation panel -----------

def status_panel(player: 'Player', # type: ignore[name-defined]
                 enemy: 'Enemy', # type: ignore[name-defined]
                 round_n: int, 
                 enemy_idX:int, 
                 enemies_total: int
                 ) -> Panel:
    """
    Generates a Panel object representing the current combat situation, including player and enemy stats, and the current round number.
    """

    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="bold", min_width=20)
    grid.add_column(min_width=26)
    grid.add_column(justify="right", min_width=12)

    grid.add_row(
        f"🧙 {player.name}",
        hp_bar(player.hp, player.max_hp),
        f"[cyan]PWR {player.power}[/cyan]",
    )
    grid.add_row(
        f"👹 {enemy.name}",
        hp_bar(enemy.hp, enemy.max_hp),
        f"[red]PWR {enemy.power}[/red]",
    )
 
    title = (
        f"[dim]Round {round_n}[/dim]  ·  "
        f"[yellow]Enemy {enemy_idX}/{enemies_total}:[/yellow] {enemy.name}"
    )
    return Panel(grid, title=title, border_style="bright_black", padding=(0, 1))

#  Menu table =-----------------

def action_table(player: 'Player') -> tuple[Table, list[str]]: # type: ignore[name-defined]
    """
    Builds the action menu for the currrent combat round.
    
    Returns the Table renderable and the list of valid choice keys
    """

    table = Table(box=box.SIMPLE, show_header=False, padding= (0,1))

    table.add_column(style= 'bold cyan', width= 3)
    table.add_column(width=12)
    table.add_column()

    table.add_row("1", "⚔️  Attack",  "Roll 1 - [cyan]PWR[/cyan] damage")
    table.add_row("2", "💨 Dodge",    "[green]75 %[/green] chance to avoid the hit entirely")
    table.add_row("3", "🛡️  Defend",   "Absorb [green]50 %[/green] of incoming damage")

    options = ["1", "2", "3"]

    if player.has_legendary:
        if player.special_ready:
            table.add_row("4", "✨ Special", "[bold yellow]READY[/bold yellow] — Roll 0 – PWR×10 damage")
        else:
            table.add_row("4", "[dim]✨ Special[/dim]",
                          f"[dim]Cooldown: {player.cooldown_remaining} round(s)[/dim]")
        options.append("4")
 
    return table, options

# ------------ Boon display --------------------------------------------
 
def boon_as_text(boon: "Boon") -> Text:  # type: ignore[name-defined]
    """Single-line Rich Text representation of a boon with rarity colour."""
    style = RARITY_STYLE[boon.rarity]
    icon  = RARITY_ICON[boon.rarity]
    t = Text()
    t.append(f"{icon} ", style=style)
    t.append(f"[{boon.rarity}] ", style=style)
    t.append(boon.name, style=f"bold {style}")
    t.append(f"  ·  {boon.god}", style="cyan")
    t.append(f"  ·  +{boon.power_bonus} POWER", style="green")
    return t
 
 
def boon_choice_table(boons: list["Boon"]) -> Table:  # type: ignore[name-defined]
    """Tabular display of 3 boon choices + a 'Decline' row."""
    table = Table(box=box.ROUNDED, header_style="bold cyan",
                  border_style="cyan", padding=(0, 1), show_lines=True)
    table.add_column("#",       style="bold",  width=3,  justify="center")
    table.add_column("Rarity",  width=12)
    table.add_column("Boon",    min_width=22)
    table.add_column("God",     style="cyan",  width=12)
    table.add_column("Bonus",   style="green", width=10, justify="right")
 
    for i, boon in enumerate(boons, 1):
        style = RARITY_STYLE[boon.rarity]
        table.add_row(
            str(i),
            Text(f"{RARITY_ICON[boon.rarity]} {boon.rarity}", style=style),
            Text(boon.name, style=f"bold {style}"),
            boon.god,
            f"+{boon.power_bonus} PWR",
        )
    table.add_row("4", "", "[dim]Decline all[/dim]", "", "")
    return table
 
 
# -------- Leaderboard  ---------
 
def leaderboard_table(records: list[dict]) -> Table:
    """Ranked leaderboard table from a list of record dicts."""
    table = Table(box=box.ROUNDED, border_style="yellow",
                  header_style="bold yellow", padding=(0, 2), show_lines=True)
    table.add_column("Rank",     justify="center", width=6)
    table.add_column("Nickname", min_width=20)
    table.add_column("Rooms",    justify="center", width=8)
 
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for i, r in enumerate(records, 1):
        color = "bold green" if i == 1 else "bold white" if i <= 3 else "dim"
        table.add_row(
            medals.get(i, str(i)),
            f"[{color}]{r['nickname']}[/{color}]",
            f"[{color}]{r['rooms']}[/{color}]",
        )
    return table