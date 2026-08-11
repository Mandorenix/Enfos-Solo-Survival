from solo_x.ecs.system import System
from solo_x.ecs.component import Position, Sprite, Health
from solo_x.systems.damage_number import DamageNumber
from typing import List, Tuple


class RenderSystem(System):
    """Handles rendering of all game entities"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
    
    def update(self, delta_time: float):
        """Update camera and prepare for rendering"""
        # Update camera to follow player
        player_pos = self.game.world.get_component(1, 'position')
        if player_pos:
            self.camera_x = player_pos.x
            self.camera_y = player_pos.y
    
    def render(self):
        """Render all entities (placeholder - actual rendering depends on backend)"""
        # This is a placeholder - actual rendering would use Pygame, OpenGL, etc.
        print("
" + "=" * 50)
        print("RENDERING FRAME")
        print("=" * 50)
        
        # Render entities by layer
        for layer in range(5):  # 0 = background, 1 = entities, 2 = projectiles, etc.
            self._render_layer(layer)
        
        # Render damage numbers
        self._render_damage_numbers()
        
        # Render UI
        self._render_ui()
    
    def _render_layer(self, layer: int):
        """Render entities on specific layer"""
        positions = self.game.world._components.get('position', {})
        sprites = self.game.world._components.get('sprite', {})
        
        for entity_id, pos in positions.items():
            sprite = sprites.get(entity_id)
            if sprite and sprite.layer == layer and sprite.visible:
                self._render_sprite(sprite, pos.x, pos.y)
    
    def _render_sprite(self, sprite: Sprite, x: float, y: float):
        """Render a single sprite"""
        # Adjust for camera
        screen_x = (x - self.camera_x) * self.zoom
        screen_y = (y - self.camera_y) * self.zoom
        
        print(f"  [{sprite.asset}] at ({screen_x:.1f}, {screen_y:.1f})")
    
    def _render_damage_numbers(self):
        """Render damage numbers"""
        dmg_system = self.game.systems.get('damage_number')
        if dmg_system:
            for dmg in dmg_system.get_all():
                screen_x = (dmg.x - self.camera_x) * self.zoom
                screen_y = (dmg.y - self.camera_y) * self.zoom
                color_name = "RED" if dmg.color == (255, 0, 0) else "GREEN" if dmg.color == (0, 255, 0) else "YELLOW"
                print(f"  [{color_name}] {dmg.value:.0f} at ({screen_x:.1f}, {screen_y:.1f})")
    
    def _render_ui(self):
        """Render UI elements"""
        print(f"
UI:")
        print(f"  Wave: {self.game.current_wave}/{self.game.max_waves}")
        print(f"  Lives: {self.game.lives}")
        print(f"  Gold: {self.game.gold}")
        print(f"  Combo: {self.game.combo}x")
        
        # Render hero info
        hero_health = self.game.world.get_component(1, 'health')
        if hero_health:
            print(f"  Hero HP: {hero_health.current:.0f}/{hero_health.max:.0f}")
        
        hero_spellbook = self.game.world.get_component(1, 'spellbook')
        if hero_spellbook:
            print(f"  Mana: {hero_spellbook.mana:.0f}/{hero_spellbook.max_mana:.0f}")
