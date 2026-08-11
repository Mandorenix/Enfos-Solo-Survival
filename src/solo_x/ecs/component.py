from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import math


@dataclass
class Position:
    """Entity position in 2D space"""
    x: float = 0.0
    y: float = 0.0
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate distance to another position"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def move_towards(self, target: 'Position', speed: float, delta_time: float):
        """Move towards target position"""
        dx = target.x - self.x
        dy = target.y - self.y
        dist = self.distance_to(target)
        
        if dist > 0:
            move_dist = min(speed * delta_time, dist)
            self.x += (dx / dist) * move_dist
            self.y += (dy / dist) * move_dist


@dataclass
class Health:
    """Entity health"""
    current: float = 100.0
    max: float = 100.0
    armor: float = 0.0
    
    @property
    def percent(self) -> float:
        """Health percentage"""
        return (self.current / self.max) * 100 if self.max > 0 else 0
    
    def take_damage(self, amount: float) -> float:
        """Take damage, return actual damage taken"""
        reduction = self.armor / (self.armor + 100)  # Armor reduces damage
        actual_damage = amount * (1 - reduction)
        self.current -= actual_damage
        if self.current < 0:
            self.current = 0
        return actual_damage
    
    def heal(self, amount: float):
        """Heal entity"""
        self.current = min(self.current + amount, self.max)
    
    def is_alive(self) -> bool:
        """Check if entity is alive"""
        return self.current > 0


@dataclass
class Damage:
    """Entity damage capabilities"""
    base: float = 20.0
    bonus: float = 0.0
    attack_speed: float = 1.0
    attack_range: float = 1.0
    
    @property
    def total(self) -> float:
        """Total damage"""
        return self.base + self.bonus
    
    def calculate_damage(self) -> float:
        """Calculate damage for this attack"""
        return self.total


@dataclass
class Sprite:
    """Entity visual representation"""
    asset: str = "default"
    width: int = 32
    height: int = 32
    visible: bool = True
    layer: int = 0  # Rendering layer


@dataclass
class AI:
    """Entity AI behavior"""
    behavior: str = "passive"  # passive, aggressive, defensive, support
    target: Optional[int] = None  # Target entity ID
    range: float = 5.0
    
    def should_attack(self, distance: float) -> bool:
        """Check if should attack based on behavior"""
        if self.behavior == "aggressive" and distance <= self.range:
            return True
        return False


@dataclass
class Movement:
    """Entity movement capabilities"""
    speed: float = 1.0
    target_x: Optional[float] = None
    target_y: Optional[float] = None
    path: List[Tuple[float, float]] = field(default_factory=list)
    
    def has_target(self) -> bool:
        """Check if has movement target"""
        return self.target_x is not None and self.target_y is not None
    
    def clear_target(self):
        """Clear movement target"""
        self.target_x = None
        self.target_y = None
        self.path = []


@dataclass
class Inventory:
    """Entity inventory"""
    items: List[str] = field(default_factory=list)
    gold: int = 0
    max_slots: int = 6
    
    def add_item(self, item_name: str) -> bool:
        """Add item to inventory"""
        if len(self.items) < self.max_slots:
            self.items.append(item_name)
            return True
        return False
    
    def remove_item(self, item_name: str) -> bool:
        """Remove item from inventory"""
        if item_name in self.items:
            self.items.remove(item_name)
            return True
        return False
    
    def has_item(self, item_name: str) -> bool:
        """Check if has item"""
        return item_name in self.items


@dataclass
class Spellbook:
    """Entity spell capabilities"""
    mana: float = 5000.0
    max_mana: float = 5000.0
    mana_regen: float = 10.0  # Mana per second
    spells: List[str] = field(default_factory=list)
    
    def cast_spell(self, spell_name: str, cost: float) -> bool:
        """Cast a spell, return True if successful"""
        if spell_name in self.spells and self.mana >= cost:
            self.mana -= cost
            return True
        return False
    
    def regenerate(self, delta_time: float):
        """Regenerate mana"""
        self.mana = min(self.mana + self.mana_regen * delta_time, self.max_mana)


@dataclass
class Team:
    """Entity team affiliation"""
    side: str = "player"  # player, enemy, neutral
    
    def is_enemy(self, other: 'Team') -> bool:
        """Check if is enemy of other team"""
        return self.side != other.side
    
    def is_ally(self, other: 'Team') -> bool:
        """Check if is ally of other team"""
        return self.side == other.side
