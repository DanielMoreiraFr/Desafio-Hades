"""
run.py
──────
Orchestrates a single run from start to finish.
This is the only module that imports from both logic/ and ui/ —
that is intentional: coordination is its sole job.

Flow:
    start_run()
        └── setup player + starting boon
        └── room loop:
              ├── combat_room()
              │     └── fight_enemy() × N
              ├── boon_offer()
              └── ask to continue or retreat
"""

import random

from entities.player  import Player
from systems.boons     import starting_boon, generate_boon_options
from systems.combat     import *
from systems.records    import save_record
from ui.console       import wait, pause
from ui.screens       import *


# ── Boon offer ────────────────────────────────────────────────────

def _boon_offer(player: Player, room: int) -> None:
    """1/3 chance to offer boons after a room."""
    if random.randint(1, 3) != 1:
        return

    god, choices = generate_boon_options(3)
    pick = show_boon_offer(god, choices, room)

    if pick == "4":
        show_boon_declined()
    else:
        chosen = choices[int(pick) - 1]
        player.add_boon(chosen)
        show_boon_acquired(chosen, player.power)
        if chosen.rarity == "Legendary":
            show_legendary_unlock()

    wait()


# ── Single-enemy fight ────────────────────────────────────────────

def _fight_enemy(player: Player, enemy, idx: int, total: int) -> bool:
    """
    Runs combat rounds against one enemy.
    Returns True if the player survived, False if they died.
    """
    show_enemy_intro(enemy, idx, total)

    round_n = 0
    while enemy.is_alive() and player.is_alive():
        round_n += 1
        player.tick_round()

        show_round_status(player, enemy, round_n, idx, total)
        choice = show_action_menu(player)

        # ── Player action ──────────────────────────────
        dodging   = False
        defending = False

        if choice == "1":
            result = player_attack(player, enemy)
            show_player_attack(enemy.name, result.damage)

        elif choice == "2":
            dodging = True
            show_dodge_stance()

        elif choice == "3":
            defending = True
            show_defend_stance()

        elif choice == "4":
            result = player_special(player, enemy)
            if result.error:
                show_special_error(result.error)
                player._cooldown -= 1   # undo tick for invalid action
                continue
            show_player_special(result.damage)

        # ── Enemy retaliation ──────────────────────────
        if enemy.is_alive():
            if dodging:
                result = enemy_attacks_dodging(player, enemy)
                if result.success:
                    show_dodge_success(enemy.name, result.damage_taken)
                else:
                    show_dodge_fail(enemy.name, result.damage_taken)
            elif defending:
                result = enemy_attacks_blocking(player, enemy)
                show_block_result(enemy.name, result.raw_damage, result.damage_taken)
            else:
                result = enemy_attacks_direct(player, enemy)
                show_direct_hit(enemy.name, result.damage)

        if not player.is_alive():
            return False

    show_enemy_defeated(enemy.name)
    return True


# ── Full room ─────────────────────────────────────────────────────

def _combat_room(player: Player, room: int) -> bool:
    """
    Spawns and fights all enemies in the room sequentially.
    Returns True if the player cleared it, False if they died.
    """
    enemies = spawn_enemies(room)
    is_boss = room % 10 == 0

    show_room_intro(room, enemies, is_boss)

    for idx, enemy in enumerate(enemies, 1):
        if not _fight_enemy(player, enemy, idx, len(enemies)):
            show_player_death(player.name, enemy.name)
            return False

    show_room_cleared(room)

    # ── Post-room healing ─────────────────────────────
    # Boss rooms restore 30 % of max HP; normal rooms restore 15 %.
    # player.heal() already caps at max_hp, so no extra guard needed.
    heal_amount = player.max_hp // 3 if is_boss else player.max_hp // 7
    player.heal(heal_amount)
    show_room_heal(player, heal_amount, is_boss)

    return True


# ── Run entry point ───────────────────────────────────────────────

def start_run() -> None:
    nickname = prompt_nickname()
    player   = Player(nickname)

    show_run_intro(player)

    # Starting boon
    boon = starting_boon()
    show_starting_boon(boon)
    player.add_boon(boon)
    if boon.rarity == "Legendary":
        show_legendary_unlock()
    wait()

    room = 1
    while True:
        survived = _combat_room(player, room)

        if not survived:
            show_run_over(player.name, room - 1, player.power)
            save_record(player.name, room - 1)
            wait("  [ENTER to return to menu]")
            return

        _boon_offer(player, room)
        show_room_summary(player, room)

        choice = show_continue_prompt(room + 1)
        if choice == "1":
            room += 1
        else:
            show_retreat(player.name)
            save_record(player.name, room)
            wait("  [ENTER to return to menu]")
            return