from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import uuid


@dataclass
class Entity:
    """Base entity class for ECS"""
    id: int
    name: str = "Entity"
    active: bool = True
    tags: list = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize entity"""
        if not hasattr(self, 'id'):
            self.id = id(self)
    
    def add_tag(self, tag: str):
        """Add tag to entity"""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove tag from entity"""
        if tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if entity has tag"""
        return tag in self.tags
    
    def destroy(self):
        """Mark entity for destruction"""
        self.active = False
