from enum import Enum, auto

class EventType(Enum):
    GAME_STARTED = auto()
    GAME_OVER = auto()

class EventBus:
    def __init__(self):
        self._subscribers = {}
    def emit(self, event_type, data=None):
        pass