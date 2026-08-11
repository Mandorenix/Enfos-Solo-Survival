from solo_x.ecs.system import System
from solo_x.ecs.component import Position, Health, Team
from solo_x.ecs.factory import EntityFactory


class BarricadeSystem(System):
    """Handles barricade placement and behavior"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.barricades = []
    
    def update(self, delta_time: float):
        """Update all barricades"""
        alive = []
        for bar_id in self.barricades[:]:
            if self._update_barricade(bar_id, delta_time):
                alive.append(bar_id)
            else:
                self.game.world.destroy_entity(bar_id)
        self.barricades = alive
    
    def _update_barricade(self, bar_id: int, delta_time: float) -> bool:
        """Update single barricade, return True if still alive"""
        health = self.game.world.get_component(bar_id, 'health')
        if health and not health.is_alive():
            return False
        return True
    
    def create_barricade(self, x: float, y: float) -> int:
        """Create a new barricade"""
        factory = EntityFactory(self.game.world)
        bar = factory.create_barricade(x, y)
        self.barricades.append(bar.id)
        
        # Add to pathfinding obstacles
        self.game.systems['pathfinding'].add_obstacle(int(x), int(y))
        
        return bar.id
    
    def destroy_barricade(self, bar_id: int):
        """Destroy a barricade"""
        if bar_id in self.barricades:
            self.barricades.remove(bar_id)
            position = self.game.world.get_component(bar_id, 'position')
            if position:
                self.game.systems['pathfinding'].remove_obstacle(
                    int(position.x), int(position.y)
                )
