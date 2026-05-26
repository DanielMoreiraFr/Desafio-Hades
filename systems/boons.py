import random
from CONFIG import GODS, RARITY_POWER, RARITY_ICON, RARITY_COLOR

class Boon:
    def __init__(self, name: str, rarity: str, god: str):
        self.name = name
        self.rarity = rarity
        self.god = god
        self.power = RARITY_POWER[rarity]
        self.icon = RARITY_ICON[rarity]

    def __str__(self):
        color = RARITY_COLOR[self.rarity]
        icon = RARITY_ICON[self.rarity]
        return f'[{color}]{icon} [{self.rarity}]: {self.name}[/]'
    
    def roll_rarity() -> str:
        """Rolls a random rarity based on predefined probabilities:
        - Common: 50%
        - Rare: 30%
        - Epic: 15%
        - Legendary: 5%
        
        Returns:
            str: The rolled rarity.
        """

        roll = random.randint(1, 100)
        if roll <= 5:
            return 'Legendary'
        if roll <= 15:
            return 'Epic'
        if roll <= 50:
            return 'Rare'
        return 'Common'
    
    def initial_roll_rarity() -> str:
        """First-room boon: Choice between Common or Rare"""
        return random.choice(['Common', 'Rare'])
    
    def produce_boon(god: str, rarity: str) -> Boon:
        """Produces a boon based on the given god and rarity.
        
        Args:
            god (str): The name of the god providing the boon.
            rarity (str): The rarity of the boon to be produced.
        Returns:
            Boon: The produced boon."""
        pool = GODS[god]["Legendary"] if rarity == 'Legendary' else GODS[god]["base"]
        return Boon(random.choice(pool), rarity, god)
    
    def starting_boon() -> Boon:
        """Generates the starting boon for the player, which is always a Common or Rare boon
        
        Returns:
            Boon: The generated starting boon."""
        god = random.choice(list(GODS.keys))
        return Boon.produce_boon(god, Boon.initial_roll_rarity())
    
    