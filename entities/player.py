from .character import Character
from random import randint, random

SPECIAL_COOLDOWN = 15

class Player(Character):
    """
    The player character, controlled by the user
    Starts with power = 30 and HP = 100
    Gains power throuh boons and loses HP when taking damage
    unlocks a especial attack once obtain an legendary boon
    """

    def __init__(self, nickname: str) -> None:
        super().__init__(nickname, power=30, hp=100)
        self.boons = []
        self.has_legendary = False
        self.cooldown = SPECIAL_COOLDOWN

# combat methods -----

    def attack(self) -> int:
        """
        Performs a normal attack
        Returns the damage dealt (a random value between 1 and the player's current power)
        """
        return randint(1, self.power)
    
    def dodge(self) -> bool:
        """
        Attempts to dodge an incoming attack
        Returns True if the dodge is successful (75% chance), False otherwise
        """
        return random() < 0.75
    
    def block(self, damage: int) -> int:
        """
        Returns the damage taken after 50% reduction
        """
        return damage // 2
    
    def try_special(self) -> tuple[int | None, str | None]:
        """
        Legendary boon needed to unlock the special attack
        If the player has a legendary boon and the special attack is not on cooldown, performs the special attack (x10 damage) and resets the cooldown

        Returns (damange, None) on sucess or (None, error_message) on failure
        """
        if not self.has_legendary:
            return None, "[red]You don't have a Legendary boon yet![/]"
        if not self.special_ready:
            return None, f'Special available in [blue]{self.cooldown_remaining} round(s)[/]!'
        damage = random.randint(1, self.power * 10)
        self.cooldown = 0
        return damage, None
    
# player boons management --

    def add_boon(self, boon) -> None:
        """
        Adds a boon to the player's inventory and updates power and legendary status if necessary
        """
        self.boons.append(boon)
        self.power += boon.power
        if boon.rarity == 'Legendary':
            self.has_legendary = True
            self.cooldown = SPECIAL_COOLDOWN

# round tick ----

    def tick_round(self) -> None:
        """
        Method to advance the special-attack cooldown by one round (should be called at the end of each round)
        """

        if self.cooldown < SPECIAL_COOLDOWN:
            self.cooldown += 1

    @property
    def special_ready(self) -> bool:
        return self.has_legendary and self.cooldown >= SPECIAL_COOLDOWN
    
    @property
    def cooldown_remaining(self) -> int:
        return max(0, SPECIAL_COOLDOWN - self.cooldown)