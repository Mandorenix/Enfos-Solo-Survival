from typing import Dict, Optional
from solo_x.ecs.entity import Entity


class World:
    """ECS World that manages all entities"""
    
    def __init__(self):
        self._entities: Dict[int, Entity] = {}
        self._next_id = 1
        self._components: Dict[str, Dict[int, object]] = {}
    
    def create_entity(self) -> Entity:
        """Create a new entity"""
        eid = self._next_id
        self._next_id += 1
        entity = Entity(eid)
        self._entities[eid] = entity
        return entity
    
    def destroy_entity(self, entity_id: int):
        """Destroy an entity and its components"""
        if entity_id in self._entities:
            # Remove all components
            for comp_type in self._components:
                if entity_id in self._components[comp_type]:
                    del self._components[comp_type][entity_id]
            del self._entities[entity_id]
    
    def get_entity(self, entity_id: int) -> Optional[Entity]:
        """Get entity by ID"""
        return self._entities.get(entity_id)
    
    def add_component(self, entity_id: int, component_type: str, component: object):
        """Add component to entity"""
        if component_type not in self._components:
            self._components[component_type] = {}
        self._components[component_type][entity_id] = component
    
    def get_component(self, entity_id: int, component_type: str) -> Optional[object]:
        """Get component from entity"""
        if component_type in self._components:
            return self._components[component_type].get(entity_id)
        return None
    
    def remove_component(self, entity_id: int, component_type: str):
        """Remove component from entity"""
        if component_type in self._components:
            if entity_id in self._components[component_type]:
                del self._components[component_type][entity_id]
    
    def get_entities_with_component(self, component_type: str) -> list:
        """Get all entities with a specific component"""
        if component_type in self._components:
            return list(self._components[component_type].keys())
        return []
    
    def update(self, delta_time: float):
        """Update all entities"""
        # TODO: Update all systems
        pass
