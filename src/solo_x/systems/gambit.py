from solo_x.ecs.system import System
from solo_x.ecs.component import Position, Health, AI, Movement, Team
from typing import Dict, Callable, List
import random


class GambitSystem(System):
    """Handles Gambit automation for AI entities"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.gambits: Dict[str, Dict] = {
            'focus_fire': {
                'condition': self._condition_lowest_hp_enemy,
                'action': self._action_attack
            },
            'protect_ally': {
                'condition': self._condition_ally_low_hp,
                'action': self._action_heal
            },
            'flee': {
                'condition': self._condition_low_hp,
                'action': self._action_flee
            },
            'harass': {
                'condition': self._condition_enemy_in_range,
                'action': self._action_attack
            },
            'guard': {
                'condition': self._condition_ally_near,
                'action': self._action_move_to_ally
            }
        }
    
    def update(self, delta_time: float):
        """Update Gambits for all AI entities"""
        ai_entities = self.game.world.get_entities_with_component('ai')
        
        for entity_id in ai_entities:
            ai = self.game.world.get_component(entity_id, 'ai')
            position = self.game.world.get_component(entity_id, 'position')
            team = self.game.world.get_component(entity_id, 'team')
            
            if ai and position and team:
                self._update_gambit(entity_id, ai, position, team)
    
    def _update_gambit(self, entity_id: int, ai: AI, position: Position, team: Team):
        """Update Gambit for entity"""
        # Find best Gambit for this entity
        for gambit_name, gambit in self.gambits.items():
            target = gambit['condition'](entity_id, position, team)
            if target:
                gambit['action'](entity_id, target)
                return
    
    def _condition_lowest_hp_enemy(self, entity_id: int, position: Position, team: Team):
        """Find enemy with lowest HP"""
        return self._find_lowest_hp_enemy(position)
    
    def _condition_ally_low_hp(self, entity_id: int, position: Position, team: Team):
        """Find ally with low HP"""
        return self._find_lowest_hp_ally(position, team)
    
    def _condition_low_hp(self, entity_id: int, position: Position, team: Team):
        """Check if self has low HP"""
        health = self.game.world.get_component(entity_id, 'health')
        if health and health.percent < 30:
            return position
        return None
    
    def _condition_enemy_in_range(self, entity_id: int, position: Position, team: Team):
        """Check if enemy in attack range"""
        ai = self.game.world.get_component(entity_id, 'ai')
        if ai:
            return self._find_enemy_in_range(position, ai.range)
        return None
    
    def _condition_ally_near(self, entity_id: int, position: Position, team: Team):
        """Check if ally nearby"""
        return self._find_ally(position, team, 3.0)
    
    def _action_attack(self, entity_id: int, target):
        """Attack target"""
        if isinstance(target, tuple):
            target_pos = target
            movement = self.game.world.get_component(entity_id, 'movement')
            if movement:
                movement.target_x, movement.target_y = target_pos
        elif isinstance(target, int):
            # TODO: Attack entity
            pass
    
    def _action_heal(self, entity_id: int, target):
        """Heal target"""
        if isinstance(target, int):
            health = self.game.world.get_component(target, 'health')
            if health:
                health.heal(50)
    
    def _action_flee(self, entity_id: int, target):
        """Flee from target"""
        if isinstance(target, tuple):
            # Move away from target
            movement = self.game.world.get_component(entity_id, 'movement')
            position = self.game.world.get_component(entity_id, 'position')
            if movement and position:
                # Move in opposite direction
                dx = position.x - target[0]
                dy = position.y - target[1]
                movement.target_x = position.x + dx * 2
                movement.target_y = position.y + dy * 2
    
    def _action_move_to_ally(self, entity_id: int, target):
        """Move to ally"""
        if isinstance(target, tuple):
            movement = self.game.world.get_component(entity_id, 'movement')
            if movement:
                movement.target_x, movement.target_y = target
    
    def _find_lowest_hp_enemy(self, position: Position):
        """Find enemy with lowest HP"""
        lowest = None
        lowest_hp = float('inf')
        
        for entity_id, pos in self.game.world._components.get('position', {}).items():
            team = self.game.world.get_component(entity_id, 'team')
            health = self.game.world.get_component(entity_id, 'health')
            
            if team and team.side == 'enemy' and health:
                dist = position.distance_to(pos)
                if dist <= 10.0 and health.current < lowest_hp:
                    lowest_hp = health.current
                    lowest = (pos.x, pos.y)
        
        return lowest
    
    def _find_lowest_hp_ally(self, position: Position, team: Team):
        """Find ally with lowest HP"""
        lowest = None
        lowest_hp = float('inf')
        
        for entity_id, pos in self.game.world._components.get('position', {}).items():
            ally_team = self.game.world.get_component(entity_id, 'team')
            health = self.game.world.get_component(entity_id, 'health')
            
            if ally_team and ally_team.side == team.side and health and entity_id != id:
                dist = position.distance_to(pos)
                if dist <= 10.0 and health.current < lowest_hp:
                    lowest_hp = health.current
                    lowest = entity_id
        
        return lowest
    
    def _find_enemy_in_range(self, position: Position, range: float):
        """Find enemy in range"""
        for entity_id, pos in self.game.world._components.get('position', {}).items():
            team = self.game.world.get_component(entity_id, 'team')
            if team and team.side == 'enemy':
                dist = position.distance_to(pos)
                if dist <= range:
                    return (pos.x, pos.y)
        return None
    
    def _find_ally(self, position: Position, team: Team, range: float):
        """Find ally in range"""
        for entity_id, pos in self.game.world._components.get('position', {}).items():
            ally_team = self.game.world.get_component(entity_id, 'team')
            if ally_team and ally_team.side == team.side and entity_id != id:
                dist = position.distance_to(pos)
                if dist <= range:
                    return (pos.x, pos.y)
        return None
