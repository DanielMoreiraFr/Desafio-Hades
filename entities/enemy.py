from .character import Character
from random import randint

class Enemy(Character):
    """Attacks directly; no special interactions"""

    def attack(self) -> int:
        return randint(1, self.power)