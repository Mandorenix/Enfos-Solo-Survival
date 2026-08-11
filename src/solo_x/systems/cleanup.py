from solo_x.ecs.system import System


class CleanupSystem(System):
    """Handles cleanup of dead entities and resources"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.dead_entities = []
    
    def update(self, delta_time: float):
        """Clean up dead entities"""
        for entity_id in self.dead_entities:
            # Remove entity from world
            # TODO: Implement entity removal
            pass
        self.dead_entities = []
    
    def mark_for_cleanup(self, entity_id: int):
        """Mark entity for cleanup"""
        if entity_id not in self.dead_entities:
            self.dead_entities.append(entity_id)
