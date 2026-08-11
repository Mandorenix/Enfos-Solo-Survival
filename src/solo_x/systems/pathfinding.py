from solo_x.ecs.system import System
from solo_x.pathfinding.grid import Grid
from solo_x.pathfinding.flow_field import FlowField
from solo_x.ecs.component import Position, Movement
import math


class PathfindingSystem(System):
    """Handles pathfinding for all entities"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.grid = Grid(128, 128)
        self.flow_field = FlowField(self.grid)
        self.target_positions = {}
    
    def update(self, delta_time: float):
        """Update pathfinding for all entities with movement"""
        # Get all entities with movement component
        movement_entities = self.game.world.get_entities_with_component('movement')
        
        for entity_id in movement_entities:
            movement = self.game.world.get_component(entity_id, 'movement')
            position = self.game.world.get_component(entity_id, 'position')
            
            if movement and position and movement.has_target():
                # Recalculate path if needed
                if not movement.path:
                    self.flow_field.calculate(int(movement.target_x), int(movement.target_y))
                    movement.path = self.flow_field.get_path(int(position.x), int(position.y))
                
                # Move along path
                if movement.path:
                    target_x, target_y = movement.path[0]
                    distance = math.sqrt((position.x - target_x) ** 2 + (position.y - target_y) ** 2)
                    
                    if distance < 0.5:  # Reached waypoint
                        movement.path.pop(0)
                        if not movement.path:
                            movement.clear_target()
                    else:
                        # Move towards waypoint
                        dx = target_x - position.x
                        dy = target_y - position.y
                        dist = math.sqrt(dx * dx + dy * dy)
                        move_dist = min(movement.speed * delta_time, dist)
                        position.x += (dx / dist) * move_dist
                        position.y += (dy / dist) * move_dist
    
    def set_target(self, entity_id: int, target_x: float, target_y: float):
        """Set target for entity"""
        movement = self.game.world.get_component(entity_id, 'movement')
        if movement:
            movement.target_x = target_x
            movement.target_y = target_y
            movement.path = []
    
    def clear_target(self, entity_id: int):
        """Clear target for entity"""
        movement = self.game.world.get_component(entity_id, 'movement')
        if movement:
            movement.clear_target()
    
    def add_obstacle(self, x: int, y: int):
        """Add obstacle to grid"""
        self.grid.set_obstacle(x, y)
    
    def remove_obstacle(self, x: int, y: int):
        """Remove obstacle from grid"""
        self.grid.clear_obstacle(x, y)
