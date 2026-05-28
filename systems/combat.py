import random
from dataclasses import dataclass
from entities.player import Player
from entities.enemy import Enemy
from CONFIG import ENEMY_NAMES, BOSS_NAMES

@dataclass
class AttackResult:
    damage: int


@dataclass
class DodgeResult:
    sucess: bool
    damage_taken: int


@dataclass
class BlockResult:
    damage_taken: int
    raw_damage:   int


@dataclass
class SpecialResult:
    damage:        int | None
    error_message: str | None


# enemy generation =--

def spawn_enemies(room: int) -> list[Enemy]:
    """
    Normal rooms: spawns 2-5 enemies, enemy power scales with room number ( power = room * 10)

    Boss rooms: spawns 1 boss, boss power scales with room number ( power = normal enemy * 5)
    """
    base_power = room * 10

    if room % 10 == 0: # Boss room
        return [Enemy(random.choice(BOSS_NAMES), power= base_power * 5, hp = 120 + room * 25)]
    count = random.randint(2, 5)
    hp = 25 + room * 8
    return [Enemy(random.choice(ENEMY_NAMES), base_power, hp) for _ in range(count)]

# player combat actions -----

def player_attack(player: Player, enemy: Enemy) -> AttackResult:
    damage = player.attack()
    enemy.take_damage(damage)

    return AttackResult(damage)

def player_special(player: Player, enemy: Enemy) -> SpecialResult:
    damage, error_message = player.try_special()
    if damage is not None:
        enemy.take_damage(damage)
    return SpecialResult(damage, error_message)

# enemies combat actions -----

def enemy_attacks_dodging(player: Player, enemy: Enemy) -> DodgeResult:
    raw = enemy.attack()
    if player.try_dodge():
        return DodgeResult(success=True, damage_taken=0)
    player.take_damage(raw)
    return DodgeResult(success=False, damage_taken=raw)

def enemy_attacks_blocking(player: Player, enemy: Enemy) -> BlockResult:
    raw     = enemy.attack()
    reduced = player.apply_block(raw)
    player.take_damage(reduced)
    return BlockResult(raw_damage=raw, damage_taken=reduced)
 
 
def enemy_attacks_direct(player: Player, enemy: Enemy) -> AttackResult:
    dmg = enemy.attack()
    player.take_damage(dmg)
    return AttackResult(damage=dmg)