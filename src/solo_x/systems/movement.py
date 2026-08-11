from solo_x.ecs.system import System
from solo_x.pathfinding.grid import Grid
from solo_x.pathfinding.flow_field import FlowField
import math


class MovementSystem(System):
    """Handles entity movement using pathfinding"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.grid = Grid()
        self.flow_field = FlowField(self.grid)
        self.targets = {}  # entity_id -> target_position
    
    def update(self, delta_time: float):
        """Update movement for all entities"""
        # TODO: Implement movement logic
        # For each entity with movement:
        # 1. Get current position
        # 2. Get target position
        # 3. Calculate path using flow field
        # 4. Move along path
        pass
    
    def set_target(self, entity_id: int, target_x: float, target_y: float):
        """Set movement target for entity"""
        self.targets[entity_id] = (target_x, target_y)
    
    def clear_target(self, entity_id: int):
        """Clear movement target for entity"""
        if entity_id in self.targets:
            del self.targets[entity_id]
    
    def get_path(self, start_x: float, start_y: float, end_x: float, end_y: float):
        """Get path from start to end using flow field"""
        # TODO: Implement flow field pathfinding
        # For now, return direct path
        return [(start_x, start_y), (end_x, end_y)]
