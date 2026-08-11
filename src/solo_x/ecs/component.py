from dataclasses import dataclass

@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0

@dataclass
class Health:
    current: float = 100.0
    max: float = 100.0

@dataclass
class Sprite:
    asset: str = "default"