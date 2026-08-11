from solo_x.ecs.system import System
from config.waves import WAVES
from config.bosses import BOSSES
import time


class WaveSystem(System):
    """Manages wave progression and timing"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.wave_start_time = 0
        self.wave_duration = 30  # seconds per wave
        self.between_wave_time = 5  # seconds between waves
        self.current_wave = 0
    
    def update(self, delta_time: float):
        """Update wave system"""
        if self.game.current_wave >= self.game.max_waves:
            return
        
        # Check if we should start next wave
        if self.current_wave < self.game.current_wave:
            self.current_wave = self.game.current_wave
            self.wave_start_time = time.time()
        
        # Check if wave time elapsed
        if self.current_wave > 0:
            elapsed = time.time() - self.wave_start_time
            if elapsed > self.wave_duration:
                # Wave completed - advance
                self.game.current_wave += 1
                self.current_wave = self.game.current_wave
                self.wave_start_time = time.time()
    
    def get_current_wave(self):
        """Get current wave info"""
        return WAVES.get_wave(self.current_wave)
    
    def is_boss_wave(self) -> bool:
        """Check if current wave is a boss wave"""
        wave = self.get_current_wave()
        return wave.boss if wave else False
    
    def get_boss(self):
        """Get boss for current wave"""
        wave = self.get_current_wave()
        if wave and wave.boss:
            return BOSSES.get_boss_by_wave(wave.wave)
        return None
