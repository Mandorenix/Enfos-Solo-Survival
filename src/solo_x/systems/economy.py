from solo_x.ecs.system import System
from config.items import ITEMS
from config.balancing import BALANCE


class EconomySystem(System):
    """Handles game economy (gold, items, crafting)"""
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.items = ITEMS
    
    def update(self, delta_time: float):
        """Update economy system"""
        # Award gold for kills
        # Handle item drops
        # Regenerate resources
        pass
    
    def add_gold(self, entity_id: int, amount: int):
        """Add gold to entity"""
        inventory = self.game.world.get_component(entity_id, 'inventory')
        if inventory:
            inventory.gold += amount
            return True
        return False
    
    def spend_gold(self, entity_id: int, amount: int) -> bool:
        """Spend gold from entity"""
        inventory = self.game.world.get_component(entity_id, 'inventory')
        if inventory and inventory.gold >= amount:
            inventory.gold -= amount
            return True
        return False
    
    def get_gold(self, entity_id: int) -> int:
        """Get gold amount for entity"""
        inventory = self.game.world.get_component(entity_id, 'inventory')
        if inventory:
            return inventory.gold
        return 0
    
    def buy_item(self, entity_id: int, item_name: str) -> bool:
        """Buy an item"""
        item = self.items.get_item(item_name)
        if not item:
            return False
        
        if self.spend_gold(entity_id, item.cost):
            inventory = self.game.world.get_component(entity_id, 'inventory')
            if inventory:
                return inventory.add_item(item_name)
        return False
    
    def sell_item(self, entity_id: int, item_name: str) -> bool:
        """Sell an item"""
        item = self.items.get_item(item_name)
        if not item:
            return False
        
        inventory = self.game.world.get_component(entity_id, 'inventory')
        if inventory and inventory.has_item(item_name):
            if inventory.remove_item(item_name):
                sell_value = int(item.cost * 0.5)  # 50% sell value
                return self.add_gold(entity_id, sell_value)
        return False
    
    def can_craft(self, entity_id: int, item_name: str) -> bool:
        """Check if can craft item"""
        item = self.items.get_item(item_name)
        if not item or not item.requires:
            return True
        
        inventory = self.game.world.get_component(entity_id, 'inventory')
        if not inventory:
            return False
        
        for req in item.requires:
            if not inventory.has_item(req):
                return False
        return True
    
    def craft_item(self, entity_id: int, item_name: str) -> bool:
        """Craft an item"""
        item = self.items.get_item(item_name)
        if not item or not self.can_craft(entity_id, item_name):
            return False
        
        inventory = self.game.world.get_component(entity_id, 'inventory')
        if not inventory:
            return False
        
        # Remove required items
        if item.requires:
            for req in item.requires:
                inventory.remove_item(req)
        
        # Add crafted item
        return inventory.add_item(item_name)
