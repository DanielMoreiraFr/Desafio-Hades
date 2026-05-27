from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, name: str, power: int, hp: int) -> None:
        self.name = name
        self.power = power
        self.hp = hp
        self.max_hp = hp

    @abstractmethod
    def attack(self) -> int:
      """Roll and return attack damage."""
 
    def is_alive(self) -> bool:
        return self.hp > 0
 
    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)
 
    def heal(self, amount: int) -> None:
        self.hp = min(self.max_hp, self.hp + amount)
 
    