import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Item:
    name: str
    category: str
    cost: int
    stats: Dict[str, float]
    requires: Optional[List[str]] = None
    special: Optional[str] = None
    risk: Optional[str] = None
    description: str = ""

class ItemsConfig:
    def __init__(self):
        self.items: Dict[str, Item] = {}
        self._load_from_json()
    
    def _load_from_json(self):
        config_path = Path(__file__).parent / "items.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                for item_data in data.get('items', []):
                    item = Item(
                        name=item_data['name'],
                        category=item_data['category'],
                        cost=item_data['cost'],
                        stats=item_data.get('stats', {}),
                        requires=item_data.get('requires'),
                        special=item_data.get('special'),
                        risk=item_data.get('risk'),
                        description=item_data.get('description', "")
                    )
                    self.items[item.name] = item
    
    def get_item(self, item_name: str) -> Optional[Item]:
        return self.items.get(item_name)
    
    def can_craft(self, item_name: str, inventory: List[str]) -> bool:
        item = self.get_item(item_name)
        if not item or not item.requires:
            return True
        for req in item.requires:
            if req not in inventory:
                return False
        return True

ITEMS = ItemsConfig()
