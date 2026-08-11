import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class BossAbility:
    name: str
    cooldown: float = 0
    description: str = ""

@dataclass
class Boss:
    id: int
    name: str
    wave: int
    health: int
    armor: int
    damage: int
    abilities: List[str]
    reward: int
    description: str

class BossesConfig:
    def __init__(self):
        self.bosses: Dict[int, Boss] = {}
        self._load_from_json()
    
    def _load_from_json(self):
        config_path = Path(__file__).parent / "bosses.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                for boss_data in data.get('bosses', []):
                    boss = Boss(
                        id=boss_data['id'],
                        name=boss_data['name'],
                        wave=boss_data['wave'],
                        health=boss_data['health'],
                        armor=boss_data['armor'],
                        damage=boss_data['damage'],
                        abilities=boss_data['abilities'],
                        reward=boss_data['reward'],
                        description=boss_data['description']
                    )
                    self.bosses[boss.id] = boss
    
    def get_boss(self, boss_id: int) -> Boss:
        return self.bosses.get(boss_id)
    
    def get_boss_by_wave(self, wave: int) -> Boss:
        for boss in self.bosses.values():
            if boss.wave == wave:
                return boss
        return None

BOSSES = BossesConfig()
