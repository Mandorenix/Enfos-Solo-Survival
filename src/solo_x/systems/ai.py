from solo_x.ecs.system import System
from config.heroes import HEROES
from config.enemies import ENEMIES
import random


class AiSystem(System):
    """Handles AI behavior for enemies and mercenaries"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.behaviors = {}
    
    def update(self, delta_time: float):
        """Update AI for all entities"""
        # TODO: Implement AI logic
        # For each AI-controlled entity:
        # 1. Determine behavior based on type
        # 2. Find target
        # 3. Execute action
        pass
    
    def register_behavior(self, entity_type: str, behavior_func):
        """Register custom behavior for entity type"""
        self.behaviors[entity_type] = behavior_func
    
    def get_target(self, entity) -> tuple:
        """Get target position for entity"""
        # TODO: Implement target selection
        # For enemies: target base
        # For mercenaries: target nearest enemy
        return (0, 0)
