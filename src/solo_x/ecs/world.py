from typing import Dict
from solo_x.ecs.entity import Entity

class World:
    def __init__(self):
        self._entities: Dict[int, Entity] = {}
        self._next_id = 1
    def create_entity(self):
        eid = self._next_id
        self._next_id += 1
        return Entity(eid)