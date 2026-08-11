import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class WaveEnemy:
    type: str
    count: int

@dataclass
class Wave:
    wave: int
    enemies: List[WaveEnemy]
    reward: int
    boss: bool = False
    boss_name: Optional[str] = None

class WavesConfig:
    def __init__(self):
        self.waves: Dict[int, Wave] = {}
        self.total_waves: int = 42
        self.difficulty_curve: str = "exponential"
        self.wave_multipliers: Dict[str, float] = {}
        self._load_from_json()
    
    def _load_from_json(self):
        config_path = Path(__file__).parent / "waves.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                self.total_waves = data.get('total_waves', 42)
                self.difficulty_curve = data.get('difficulty_curve', 'exponential')
                self.wave_multipliers = data.get('wave_multipliers', {})
                
                for wave_data in data.get('waves', []):
                    wave = Wave(
                        wave=wave_data['wave'],
                        enemies=[WaveEnemy(**e) for e in wave_data['enemies']],
                        reward=wave_data['reward'],
                        boss=wave_data.get('boss', False),
                        boss_name=wave_data.get('boss_name')
                    )
                    self.waves[wave.wave] = wave
    
    def get_wave(self, wave_number: int) -> Optional[Wave]:
        return self.waves.get(wave_number)
    
    def get_all_waves(self) -> List[Wave]:
        return sorted(self.waves.values(), key=lambda w: w.wave)

WAVES = WavesConfig()
