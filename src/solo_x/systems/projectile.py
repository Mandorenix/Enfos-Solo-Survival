from solo_x.ecs.system import System
from solo_x.ecs.component import Position, Movement, Damage, Team
from solo_x.ecs.factory import EntityFactory
from config.enemies import ENEMIES


class ProjectileSystem(System):
    """Handles projectile movement and collision"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.projectiles = []
    
    def update(self, delta_time: float):
        """Update all projectiles"""
        alive = []
        for proj_id in self.projectiles[:]:
            if self._update_projectile(proj_id, delta_time):
                alive.append(proj_id)
            else:
                self.game.world.destroy_entity(proj_id)
        self.projectiles = alive
    
    def _update_projectile(self, proj_id: int, delta_time: float) -> bool:
        """Update single projectile, return True if still alive"""
        position = self.game.world.get_component(proj_id, 'position')
        movement = self.game.world.get_component(proj_id, 'movement')
        damage = self.game.world.get_component(proj_id, 'damage')
        team = self.game.world.get_component(proj_id, 'team')
        
        if not position or not movement:
            return False
        
        # Move projectile
        if movement.has_target():
            dx = movement.target_x - position.x
            dy = movement.target_y - position.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            
            if dist < 0.5:
                # Hit target - apply damage and destroy
                self._apply_damage(proj_id, damage)
                return False
            else:
                move_dist = min(movement.speed * delta_time, dist)
                position.x += (dx / dist) * move_dist
                position.y += (dy / dist) * move_dist
        
        return True
    
    def _apply_damage(self, proj_id: int, damage_comp: Damage):
        """Apply projectile damage to target"""
        team = self.game.world.get_component(proj_id, 'team')
        if not team:
            return
        
        # Find entities at target position
        for entity_id, pos in self.game.world._components.get('position', {}).items():
            entity_team = self.game.world.get_component(entity_id, 'team')
            if entity_team and entity_team.is_enemy(team):
                # Check distance
                if abs(pos.x - damage_comp.target_x) < 1.0 and abs(pos.y - damage_comp.target_y) < 1.0:
                    health = self.game.world.get_component(entity_id, 'health')
                    if health:
                        health.take_damage(damage_comp.total)
                        self.game.systems['damage_number'].add_damage_number(
                            damage_comp.total, pos.x, pos.y
                        )
    
    def create_projectile(self, owner_id: int, target_x: float, target_y: float, damage: float = 50) -> int:
        """Create a new projectile"""
        factory = EntityFactory(self.game.world)
        proj = factory.create_projectile(owner_id, target_x, target_y, damage)
        self.projectiles.append(proj.id)
        return proj.id
