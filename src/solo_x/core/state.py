from enum import Enum, auto
from dataclasses import dataclass

class GamePhase(Enum):
    PLAYING = auto()
    GAME_OVER = auto()

@dataclass
class GameState:
    phase: GamePhase = GamePhase.PLAYING