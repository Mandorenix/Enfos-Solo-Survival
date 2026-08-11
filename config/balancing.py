import json
from pathlib import Path
from dataclasses import dataclass

@dataclass
class BalanceValues:
    starting_lives: int = 100
    max_waves: int = 42
    target_fps: int = 60

@dataclass
class DifficultySettings:
    health_multiplier: float = 1.0
    damage_multiplier: float = 1.0
    gold_multiplier: float = 1.0

@dataclass
class HeroBalance:
    base_hp: int = 1200
    hp_growth: int = 150
    armor_growth: int = 10

@dataclass
class EnemyBalance:
    base_hp: int = 100
    base_damage: int = 20
    hp_growth_per_wave: float = 1.15
    damage_growth_per_wave: float = 1.12
    speed_variation: float = 0.2

@dataclass
class GameSettings:
    starting_lives: int = 100
    max_waves: int = 42
    target_fps: int = 60
    base_gold: int = 100
    gold_multiplier: float = 1.15
    combo_multiplier: float = 1.1
    max_combo: int = 100

class BalanceConfig:
    def __init__(self):
        self.game_settings = GameSettings()
        self.difficulty = {}
        self.hero_balance = {}
        self.enemy_balance = EnemyBalance()
        self._load_from_json()
    
    def _load_from_json(self):
        config_path = Path(__file__).parent / "balancing.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                
                if 'game_settings' in data:
                    self.game_settings = GameSettings(**data['game_settings'])
                
                if 'difficulty' in data:
                    for diff, settings in data['difficulty'].items():
                        self.difficulty[diff] = DifficultySettings(**settings)
                
                if 'hero_balance' in data:
                    for role, balance in data['hero_balance'].items():
                        self.hero_balance[role] = HeroBalance(**balance)
                
                if 'enemy_balance' in data:
                    self.enemy_balance = EnemyBalance(**data['enemy_balance'])

BALANCE = BalanceConfig()
