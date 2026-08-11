from dataclasses import dataclass

@dataclass
class BalanceValues:
    starting_lives: int = 100
    max_waves: int = 42
    target_fps: int = 60

BALANCE = BalanceValues()