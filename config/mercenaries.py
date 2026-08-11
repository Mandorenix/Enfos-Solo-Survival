import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Mercenary:
    id: int
    name: str
    cost: int
    stats: Dict[str, float]
    role: str
    description: str

class MercenariesConfig:
    def __init__(self):
        self.mercenaries: Dict[int, Mercenary] = {}
        self.max_mercenaries: int = 10
        self.upgrade_system: bool = True
        self._load_from_json()
    
    def _load_from_json(self):
        config_path = Path(__file__).parent / "mercenaries.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                self.max_mercenaries = data.get('max_mercenaries', 10)
                self.upgrade_system = data.get('upgrade_system', True)
                
                for merc_data in data.get('mercenaries', []):
                    merc = Mercenary(
                        id=merc_data['id'],
                        name=merc_data['name'],
                        cost=merc_data['cost'],
                        stats=merc_data['stats'],
                        role=merc_data['role'],
                        description=merc_data['description']
                    )
                    self.mercenaries[merc.id] = merc
    
    def get_mercenary(self, merc_id: int) -> Mercenary:
        return self.mercenaries.get(merc_id)

MERCENARIES = MercenariesConfig()
