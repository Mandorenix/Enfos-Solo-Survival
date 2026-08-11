from solo_x.ecs.system import System
from dataclasses import dataclass
from typing import List, Tuple
import time


@dataclass
class DamageNumber:
    """Floating damage number"""
    value: float
    x: float
    y: float
    color: Tuple[int, int, int] = (255, 0, 0)  # Red for damage
    lifetime: float = 1.0
    speed: float = 50.0
    size: float = 16.0
    created_at: float = 0.0
    
    def update(self, delta_time: float) -> bool:
        """Update damage number, return True if still alive"""
        self.y -= self.speed * delta_time
        self.lifetime -= delta_time
        return self.lifetime > 0


class DamageNumberSystem(System):
    """Handles floating damage numbers"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.damage_numbers: List[DamageNumber] = []
    
    def update(self, delta_time: float):
        """Update all damage numbers"""
        alive = []
        for dmg in self.damage_numbers:
            if dmg.update(delta_time):
                alive.append(dmg)
        self.damage_numbers = alive
    
    def add_damage_number(self, value: float, x: float, y: float, color: Tuple[int, int, int] = None):
        """Add a new damage number"""
        dmg = DamageNumber(
            value=value,
            x=x,
            y=y,
            color=color or (255, 0, 0)
        )
        self.damage_numbers.append(dmg)
        return dmg
    
    def add_heal_number(self, value: float, x: float, y: float):
        """Add a heal number (green)"""
        return self.add_damage_number(value, x, y, (0, 255, 0))
    
    def add_gold_number(self, value: float, x: float, y: float):
        """Add a gold number (yellow)"""
        return self.add_damage_number(value, x, y, (255, 255, 0))
    
    def get_all(self) -> List[DamageNumber]:
        """Get all active damage numbers"""
        return self.damage_numbers
