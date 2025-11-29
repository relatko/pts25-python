from dataclasses import dataclass
from .activation_pattern import ActivationPattern
from .scoring_method import ScoringMethod
from .grid import Grid

@dataclass
class Player:
    id: int
    activation_patterns: list[ActivationPattern]
    scoring_methods: list[ScoringMethod]
    grid: Grid
    
    def __post_init__(self) -> None:
        if len(self.activation_patterns) != 2:
            raise Exception("Incorrect number of activation patterns")
        if len(self.scoring_methods) != 2:
            raise Exception("Incorrect number of scoring methods")
