import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Enemy:
    id: str
    name: str
    health: int = 100
    armor: int = 0
    damage: int = 20
    speed: float = 1.0
    description: str = ""

class EnemiesConfig:
    def __init__(self):
        self.enemies: Dict[str, Enemy] = {}
        self._load_defaults()
    
    def _load_defaults(self):
        # Default enemies
        self.enemies = {
            "goblin": Enemy("goblin", "Goblin", 100, 5, 25, 1.0, "Basic melee enemy"),
            "skeleton": Enemy("skeleton", "Skeleton", 80, 10, 30, 0.9, "Undead melee enemy"),
            "ogre": Enemy("ogre", "Ogre", 300, 20, 60, 0.8, "Heavy melee enemy"),
            "zombie": Enemy("zombie", "Zombie", 120, 0, 20, 0.7, "Slow undead enemy"),
            "demon": Enemy("demon", "Demon", 200, 15, 50, 1.1, "Fast demonic enemy"),
            "hellhound": Enemy("hellhound", "Hellhound", 150, 10, 40, 1.3, "Fast ranged enemy"),
            "necromancer": Enemy("necromancer", "Necromancer", 100, 5, 40, 0.8, "Caster enemy that raises dead")
        }
    
    def get_enemy(self, enemy_id: str) -> Enemy:
        return self.enemies.get(enemy_id)

ENEMIES = EnemiesConfig()
