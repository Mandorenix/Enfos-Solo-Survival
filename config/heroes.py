import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class HeroStats:
    hp: int = 1000
    armor: int = 0
    damage: int = 100
    agi: int = 10
    str: int = 10
    int: int = 10

@dataclass
class Hero:
    id: int
    name: str
    symbol: str
    category: str
    core_items: List[str]
    stats: HeroStats
    description: str

class HeroesConfig:
    def __init__(self):
        self.heroes: Dict[int, Hero] = {}
        self.categories: Dict[str, Dict[str, Any]] = {}
        self._load_from_json()
    
    def _load_from_json(self):
        config_path = Path(__file__).parent / "heroes.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                
                for hero_data in data.get('heroes', []):
                    hero = Hero(
                        id=hero_data['id'],
                        name=hero_data['name'],
                        symbol=hero_data['symbol'],
                        category=hero_data['category'],
                        core_items=hero_data['core_items'],
                        stats=HeroStats(**hero_data['stats']),
                        description=hero_data['description']
                    )
                    self.heroes[hero.id] = hero
                
                self.categories = data.get('categories', {})
    
    def get_hero(self, hero_id: int) -> Hero:
        return self.heroes.get(hero_id)
    
    def get_heroes_by_category(self, category: str) -> List[Hero]:
        return [h for h in self.heroes.values() if h.category.lower() == category.lower()]
    
    def get_all_heroes(self) -> List[Hero]:
        return list(self.heroes.values())

HEROES = HeroesConfig()
