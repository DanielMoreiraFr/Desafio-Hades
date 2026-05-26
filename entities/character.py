from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, name: str, strength: int, hp: int):
        self.name = name
        self.strength = strength
        self.hp = hp

    @abstractmethod
    def attack(self, other):
        pass

    