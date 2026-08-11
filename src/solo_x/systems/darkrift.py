from solo_x.ecs.system import System
from solo_x.ecs.component import Position, Health, Team
from config.balancing import BALANCE
import random


class DarkriftSystem(System):
    """Handles Darkrift spell - summons additional enemies"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.cooldown = 30.0  # seconds
        self.current_cooldown = 0.0
        self.mana_cost = 1000
    
    def update(self, delta_time: float):
        """Update cooldown"""
        if self.current_cooldown > 0:
            self.current_cooldown -= delta_time
    
    def can_cast(self) -> bool:
        """Check if can cast Darkrift"""
        spellbook = self.game.world.get_component(1, 'spellbook')  # Player
        return (spellbook and spellbook.mana >= self.mana_cost and 
                self.current_cooldown <= 0)
    
    def cast(self, target_x: float, target_y: float) -> bool:
        """Cast Darkrift at position"""
        if not self.can_cast():
            return False
        
        spellbook = self.game.world.get_component(1, 'spellbook')
        if not spellbook:
            return False
        
        # Spend mana
        spellbook.mana -= self.mana_cost
        self.current_cooldown = self.cooldown
        
        # Summon enemies
        enemy_types = ['goblin', 'skeleton', 'zombie']
        for _ in range(5):  # Summon 5 enemies
            enemy_type = random.choice(enemy_types)
            self.game.systems['spawn'].spawn_enemy(enemy_type, target_x, target_y)
        
        return True
