from .character import Character
from random import randint
from rich import print
from time import sleep

class Enemy(Character):
    def __init__(self, name: str, strength: int, hp: int):
        super().__init__(name, strength, hp)

    def attack(self, other):
        damage = randint(1, self.strength)
        other.hp -= damage
        print(f'[red]{self.name}[/] attacks [blue]{other.name}[/]!')
        sleep(1)
        print(f'[blue]{other.name}[/] has [green]{other.hp}[/] HP left.')