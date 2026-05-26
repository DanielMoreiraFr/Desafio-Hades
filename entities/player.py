from .character import Character
from random import randint
from rich import print

class Zagreus(Character):
    def __init__(self, name: str, strength: int, hp: int):
        super().__init__(name, strength, hp)
        self.boons = []

    def attack(self, other):
        damage = randint(1, self.strength)
        other.hp -= damage
        print(f'[blue]{self.name}[/] attacks [red]{other.name}[/]!')
        print(f'[red]{other.name}[/] has [green]{other.hp}[/] HP left.')