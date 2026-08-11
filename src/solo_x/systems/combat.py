from solo_x.ecs.system import System
from config.heroes import HEROES
from config.enemies import ENEMIES
import random


class CombatSystem(System):
    """Handles combat between entities"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.combo_multiplier = 1.0
        self.current_combo = 0
    
    def update(self, delta_time: float):
        """Update combat system"""
        # TODO: Implement combat logic
        # For now, just demo combo system
        pass
    
    def attack(self, attacker, target, damage: float):
        """Perform an attack"""
        # Apply damage
        target_hp = getattr(target, 'health', 100)
        new_hp = target_hp - damage
        
        if self.game.verbose:
            print(f"{attacker} attacks {target} for {damage:.1f} damage!")
        
        # Increment combo
        self.current_combo += 1
        self.combo_multiplier = 1.0 + (self.current_combo * 0.01)
        
        # Cap combo
        if self.current_combo > self.game.max_combo:
            self.game.max_combo = self.current_combo
        
        # TODO: Check if target is dead
        # TODO: Award gold
        
        return new_hp <= 0
    
    def reset_combo(self):
        """Reset combo counter"""
        self.current_combo = 0
        self.combo_multiplier = 1.0
    
    def get_combo_bonus(self) -> float:
        """Get current combo multiplier"""
        return self.combo_multiplier
