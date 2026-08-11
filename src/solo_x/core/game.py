from solo_x.core.state import GameState, GamePhase
from solo_x.ecs.world import World
from solo_x.ecs.entity import Entity
from config.balancing import BALANCE
from config.heroes import HEROES
from config.waves import WAVES
from config.bosses import BOSSES
from config.enemies import ENEMIES
from config.items import ITEMS
from config.mercenaries import MERCENARIES
import time
import random
from typing import Optional, List


class Game:
    """Main game class"""
    
    def __init__(self, hero_id: int = 1, max_waves: int = 42, 
                 target_fps: int = 60, seed: Optional[int] = None,
                 verbose: bool = False):
        self.hero_id = hero_id
        self.max_waves = max_waves
        self.target_fps = target_fps
        self.seed = seed
        self.verbose = verbose
        self._running = False
        self._paused = False
        
        # Initialize random seed
        if seed is not None:
            random.seed(seed)
        
        # Game state
        self.state = GameState()
        self.world = World()
        self.current_wave = 0
        self.lives = BALANCE.game_settings.starting_lives
        self.gold = BALANCE.game_settings.base_gold
        self.combo = 0
        self.max_combo = 0
        
        # Load hero
        self.hero = HEROES.get_hero(hero_id)
        if self.hero is None:
            self.hero = HEROES.get_hero(1)  # Default to first hero
        
        # Initialize systems
        self._init_systems()
        
        if verbose:
            print(f"Game initialized with hero: {self.hero.name}")
            print(f"Starting lives: {self.lives}")
            print(f"Max waves: {self.max_waves}")
    
    def _init_systems(self):
        """Initialize game systems"""
        # Import and initialize all systems
        from solo_x.systems.wave import WaveSystem
        from solo_x.systems.spawn import SpawnSystem
        from solo_x.systems.ai import AiSystem
        from solo_x.systems.combat import CombatSystem
        from solo_x.systems.movement import MovementSystem
        from solo_x.systems.cleanup import CleanupSystem
        
        self.systems = {
            'wave': WaveSystem(self),
            'spawn': SpawnSystem(self),
            'ai': AiSystem(self),
            'combat': CombatSystem(self),
            'movement': MovementSystem(self),
            'cleanup': CleanupSystem(self)
        }
    
    def start(self):
        """Start the game"""
        self._running = True
        self.state.phase = GamePhase.PLAYING
        print(f"
Game started! Wave 1 incoming...")
    
    def stop(self):
        """Stop the game"""
        self._running = False
        self.state.phase = GamePhase.GAME_OVER
    
    def pause(self):
        """Pause the game"""
        self._paused = True
    
    def resume(self):
        """Resume the game"""
        self._paused = False
    
    def next_wave(self):
        """Advance to next wave"""
        self.current_wave += 1
        wave = WAVES.get_wave(self.current_wave)
        if wave:
            print(f"
=== Wave {self.current_wave} ===")
            for enemy_group in wave.enemies:
                print(f"  {enemy_group.count}x {enemy_group.type}")
            print(f"  Reward: {wave.reward}g")
            
            # Spawn enemies
            for enemy_group in wave.enemies:
                for _ in range(enemy_group.count):
                    enemy_data = ENEMIES.get_enemy(enemy_group.type)
                    if enemy_data:
                        entity = self.world.create_entity()
                        # TODO: Add enemy component with data
            
            # Check if boss wave
            if wave.boss:
                boss = BOSSES.get_boss_by_wave(self.current_wave)
                if boss:
                    print(f"  ⚠️  BOSS: {boss.name} ({boss.health} HP)")
        else:
            print(f"
✅ All {self.current_wave - 1} waves completed!")
            self.state.phase = GamePhase.GAME_OVER
            self._running = False
    
    def run(self):
        """Main game loop (headless)"""
        self.start()
        
        last_time = time.time()
        frame_count = 0
        
        while self._running and self.current_wave < self.max_waves:
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time
            
            # Cap delta time
            delta_time = min(delta_time, 0.1)
            
            # Update systems
            for name, system in self.systems.items():
                system.update(delta_time)
            
            # Check for wave completion
            if self._should_next_wave():
                self.next_wave()
            
            # Control FPS
            frame_count += 1
            if frame_count % self.target_fps == 0:
                if self.verbose:
                    fps = frame_count / (current_time - (last_time - delta_time))
                    print(f"FPS: {fps:.1f} | Wave: {self.current_wave} | Lives: {self.lives} | Gold: {self.gold}")
            
            # Sleep to maintain FPS
            sleep_time = (1.0 / self.target_fps) - (time.time() - current_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        print(f"
Game over! Completed {self.current_wave} waves.")
    
    def run_demo(self):
        """Demo mode - auto-play through waves"""
        print("
=== DEMO MODE ===")
        self.start()
        
        for wave_num in range(1, min(self.max_waves, 11)):
            wave = WAVES.get_wave(wave_num)
            if wave:
                print(f"
Wave {wave_num}:")
                for enemy_group in wave.enemies:
                    enemy = ENEMIES.get_enemy(enemy_group.type)
                    if enemy:
                        print(f"  {enemy_group.count}x {enemy.name} (HP: {enemy.health}, Dmg: {enemy.damage})")
                print(f"  Reward: {wave.reward}g")
                if wave.boss:
                    boss = BOSSES.get_boss_by_wave(wave_num)
                    if boss:
                        print(f"  👹 BOSS: {boss.name}")
            time.sleep(1)
        
        print("
Demo completed!")
    
    def _should_next_wave(self) -> bool:
        """Check if we should advance to next wave"""
        # TODO: Implement wave completion logic
        # For now, auto-advance every 3 seconds in demo
        return False
    
    def add_gold(self, amount: int):
        """Add gold to player"""
        self.gold += amount
        if self.verbose:
            print(f"+{amount}g (Total: {self.gold}g)")
    
    def spend_gold(self, amount: int) -> bool:
        """Spend gold, return True if successful"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def take_damage(self, amount: int):
        """Take damage to base lives"""
        self.lives -= amount
        if self.lives <= 0:
            self.lives = 0
            self._running = False
            self.state.phase = GamePhase.GAME_OVER
        if self.verbose:
            print(f"-{amount} lives (Remaining: {self.lives})")
