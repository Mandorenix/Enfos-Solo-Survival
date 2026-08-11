from solo_x.ecs.world import World
from solo_x.ecs.entity import Entity
from solo_x.ecs.component import Position, Health, Damage, Sprite, AI, Movement, Team, Inventory, Spellbook
from config.heroes import HEROES
from config.enemies import ENEMIES
from config.bosses import BOSSES
from typing import Optional


class EntityFactory:
    """Factory for creating game entities"""
    
    def __init__(self, world: World):
        self.world = world
        self._next_id = 1
    
    def create_hero(self, hero_id: int, x: float = 0, y: float = 0) -> Entity:
        """Create a hero entity"""
        hero_data = HEROES.get_hero(hero_id)
        if not hero_data:
            hero_data = HEROES.get_hero(1)
        
        entity = self.world.create_entity()
        
        # Add components
        self.world.add_component(entity.id, 'position', Position(x, y))
        self.world.add_component(entity.id, 'health', Health(
            current=hero_data.stats.hp,
            max=hero_data.stats.hp,
            armor=hero_data.stats.armor
        ))
        self.world.add_component(entity.id, 'damage', Damage(
            base=hero_data.stats.damage,
            attack_speed=1.0
        ))
        self.world.add_component(entity.id, 'sprite', Sprite(
            asset=hero_data.symbol,
            width=32,
            height=32
        ))
        self.world.add_component(entity.id, 'ai', AI(
            behavior="aggressive",
            range=5.0
        ))
        self.world.add_component(entity.id, 'movement', Movement(
            speed=1.0
        ))
        self.world.add_component(entity.id, 'team', Team(side="player"))
        self.world.add_component(entity.id, 'inventory', Inventory(
            gold=100,
            max_slots=6
        ))
        self.world.add_component(entity.id, 'spellbook', Spellbook(
            mana=5000,
            max_mana=5000
        ))
        
        # Add hero-specific tags
        entity.add_tag('hero')
        entity.add_tag(hero_data.category.lower())
        entity.name = hero_data.name
        
        return entity
    
    def create_enemy(self, enemy_type: str, x: float = 0, y: float = 0) -> Optional[Entity]:
        """Create an enemy entity"""
        enemy_data = ENEMIES.get_enemy(enemy_type)
        if not enemy_data:
            return None
        
        entity = self.world.create_entity()
        
        # Add components
        self.world.add_component(entity.id, 'position', Position(x, y))
        self.world.add_component(entity.id, 'health', Health(
            current=enemy_data.health,
            max=enemy_data.health,
            armor=enemy_data.armor
        ))
        self.world.add_component(entity.id, 'damage', Damage(
            base=enemy_data.damage,
            attack_speed=1.0
        ))
        self.world.add_component(entity.id, 'sprite', Sprite(
            asset="E",  # Enemy symbol
            width=32,
            height=32
        ))
        self.world.add_component(entity.id, 'ai', AI(
            behavior="aggressive",
            range=2.0
        ))
        self.world.add_component(entity.id, 'movement', Movement(
            speed=enemy_data.speed
        ))
        self.world.add_component(entity.id, 'team', Team(side="enemy"))
        
        # Add enemy tags
        entity.add_tag('enemy')
        entity.add_tag(enemy_type)
        entity.name = enemy_data.name
        
        return entity
    
    def create_boss(self, boss_id: int, x: float = 0, y: float = 0) -> Optional[Entity]:
        """Create a boss entity"""
        boss = BOSSES.get_boss(boss_id)
        if not boss:
            return None
        
        entity = self.world.create_entity()
        
        # Add components
        self.world.add_component(entity.id, 'position', Position(x, y))
        self.world.add_component(entity.id, 'health', Health(
            current=boss.health,
            max=boss.health,
            armor=boss.armor
        ))
        self.world.add_component(entity.id, 'damage', Damage(
            base=boss.damage,
            attack_speed=0.8
        ))
        self.world.add_component(entity.id, 'sprite', Sprite(
            asset="B",  # Boss symbol
            width=48,
            height=48
        ))
        self.world.add_component(entity.id, 'ai', AI(
            behavior="aggressive",
            range=3.0
        ))
        self.world.add_component(entity.id, 'movement', Movement(
            speed=0.8
        ))
        self.world.add_component(entity.id, 'team', Team(side="enemy"))
        
        # Add boss tags and abilities
        entity.add_tag('boss')
        entity.add_tag('enemy')
        for ability in boss.abilities:
            entity.add_tag(f'ability:{ability}')
        entity.name = boss.name
        
        return entity
    
    def create_mercenary(self, merc_id: int, x: float = 0, y: float = 0) -> Optional[Entity]:
        """Create a mercenary entity"""
        # TODO: Implement when mercenaries config is complete
        return self.create_enemy("footman", x, y)
    
    def create_projectile(self, owner_id: int, target_x: float, target_y: float, damage: float = 50) -> Entity:
        """Create a projectile entity"""
        entity = self.world.create_entity()
        
        # Add components
        self.world.add_component(entity.id, 'position', Position(0, 0))
        self.world.add_component(entity.id, 'damage', Damage(base=damage))
        self.world.add_component(entity.id, 'movement', Movement(
            speed=5.0,
            target_x=target_x,
            target_y=target_y
        ))
        self.world.add_component(entity.id, 'sprite', Sprite(
            asset="*",
            width=8,
            height=8
        ))
        
        # Add projectile tags
        entity.add_tag('projectile')
        entity.add_tag('damage_dealer')
        entity.name = "Projectile"
        
        return entity
    
    def create_barricade(self, x: float, y: float) -> Entity:
        """Create a barricade entity"""
        entity = self.world.create_entity()
        
        # Add components
        self.world.add_component(entity.id, 'position', Position(x, y))
        self.world.add_component(entity.id, 'health', Health(
            current=500,
            max=500,
            armor=20
        ))
        self.world.add_component(entity.id, 'sprite', Sprite(
            asset="#",
            width=32,
            height=32
        ))
        self.world.add_component(entity.id, 'team', Team(side="player"))
        
        # Add barricade tags
        entity.add_tag('barricade')
        entity.add_tag('obstacle')
        entity.name = "Barricade"
        
        return entity
