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

