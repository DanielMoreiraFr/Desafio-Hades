import random
from CONFIG import GODS, RARITY_POWER

class Boon:
    def __init__(self, name: str, rarity: str, god: str) -> None:
        self.name = name
        self.rarity = rarity
        self.god = god
        self.power = RARITY_POWER[rarity]

    def __repr__(self) -> str:
        return f"Boon({self.name!r}, {self.rarity!r}, {self.god!r})"
    
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
    
# boon generation methods -----

    def make_boon(god: str, rarity: str) -> Boon:
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
        god = random.choice(list(GODS))
        return Boon.make_boon(god, Boon.initial_roll_rarity())
    
    def generate_boon_options(count: int = 3) -> tuple[str, list[Boon]]:
        """Generates a set of boon options for the player to choose from after a victory.
        
        Args:
            count (int, optional): The number of boon options to generate. Defaults to 3.
        Returns:
            tuple[str, list[Boon]]: A tuple containing the name of the god providing the boons and a list of the generated boon options.
        """
        god = random.choice(list(GODS))
        boons = [Boon.make_boon(god, Boon.roll_rarity()) for _ in range(count)]
        return god, boons