from solo_x.ecs.system import System
from solo_x.ecs.component import Position, Spellbook, Health
from config.items import ITEMS
import random


class SpellSystem(System):
    """Handles spell casting and effects"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.spells = {
            'mana_burn': {'cost': 500, 'cooldown': 15, 'effect': self._cast_mana_burn},
            'stun': {'cost': 800, 'cooldown': 20, 'effect': self._cast_stun},
            'darkrift': {'cost': 1000, 'cooldown': 30, 'effect': self._cast_darkrift},
            'arhat': {'cost': 2000, 'cooldown': 60, 'effect': self._cast_arhat}
        }
        self.cooldowns = {}
    
    def update(self, delta_time: float):
        """Update spell cooldowns"""
        for spell_name in list(self.cooldowns.keys()):
            self.cooldowns[spell_name] -= delta_time
            if self.cooldowns[spell_name] <= 0:
                del self.cooldowns[spell_name]
    
    def cast(self, entity_id: int, spell_name: str, target_x: float = 0, target_y: float = 0) -> bool:
        """Cast a spell"""
        if spell_name not in self.spells:
            return False
        
        spell = self.spells[spell_name]
        
        # Check cooldown
        if spell_name in self.cooldowns:
            return False
        
        # Check mana
        spellbook = self.game.world.get_component(entity_id, 'spellbook')
        if not spellbook or spellbook.mana < spell['cost']:
            return False
        
        # Cast spell
        spellbook.mana -= spell['cost']
        self.cooldowns[spell_name] = spell['cooldown']
        
        # Apply effect
        return spell['effect'](entity_id, target_x, target_y)
    
    def _cast_mana_burn(self, caster_id: int, target_x: float, target_y: float) -> bool:
        """Mana Burn: Reduces enemy mana and deals damage"""
        # Find enemies near target
        enemies = self._get_enemies_near(target_x, target_y, 5.0)
        for enemy_id in enemies:
            health = self.game.world.get_component(enemy_id, 'health')
            if health:
                health.take_damage(100)
        return True
    
    def _cast_stun(self, caster_id: int, target_x: float, target_y: float) -> bool:
        """Stun: Temporarily disables enemies"""
        enemies = self._get_enemies_near(target_x, target_y, 5.0)
        for enemy_id in enemies:
            # TODO: Add stun component
            pass
        return True
    
    def _cast_darkrift(self, caster_id: int, target_x: float, target_y: float) -> bool:
        """Darkrift: Summon additional enemies"""
        return self.game.systems['darkrift'].cast(target_x, target_y)
    
    def _cast_arhat(self, caster_id: int, target_x: float, target_y: float) -> bool:
        """Arhat: Summon Arhat entity with attack speed aura"""
        # TODO: Implement Arhat summoning
        return True
    
    def _get_enemies_near(self, x: float, y: float, radius: float) -> list:
        """Get enemy IDs near position"""
        enemies = []
        for entity_id, position in self.game.world._components.get('position', {}).items():
            team = self.game.world.get_component(entity_id, 'team')
            if team and team.side == 'enemy':
                dist = ((position.x - x) ** 2 + (position.y - y) ** 2) ** 0.5
                if dist <= radius:
                    enemies.append(entity_id)
        return enemies
