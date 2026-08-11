from solo_x.ecs.system import System
from solo_x.ecs.world import World
from solo_x.ecs.entity import Entity
from config.enemies import ENEMIES
from config.bosses import BOSSES
import random


class SpawnSystem(System):
    """Handles spawning of enemies and bosses"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.spawn_points = []
        self._init_spawn_points()
    
    def _init_spawn_points(self):
        """Initialize spawn points"""
        # TODO: Load from map data
        self.spawn_points = [
            (0, 0), (10, 0), (20, 0)  # Top row
        ]
    
    def update(self, delta_time: float):
        """Update spawn system"""
        wave = self.game.systems['wave'].get_current_wave()
        if not wave:
            return
        
        # Spawn enemies for current wave
        for enemy_group in wave.enemies:
            for _ in range(enemy_group.count):
                self.spawn_enemy(enemy_group.type)
    
    def spawn_enemy(self, enemy_type: str) -> Entity:
        """Spawn an enemy of given type"""
        enemy_data = ENEMIES.get_enemy(enemy_type)
        if not enemy_data:
            return None
        
        # Create entity
        entity = self.game.world.create_entity()
        
        # TODO: Add enemy component with data
        if self.game.verbose:
            print(f"Spawned {enemy_type} at {self.spawn_points[0]}")
        
        return entity
    
    def spawn_boss(self, boss_id: int) -> Entity:
        """Spawn a boss"""
        boss = BOSSES.get_boss(boss_id)
        if not boss:
            return None
        
        # Create entity
        entity = self.game.world.create_entity()
        
        # TODO: Add boss component with data
        if self.game.verbose:
            print(f"Spawned BOSS: {boss.name} ({boss.health} HP)")
        
        return entity
