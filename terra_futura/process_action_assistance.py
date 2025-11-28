from .card import Card
from .grid import Grid
from .simple_types import Resource, GridPosition

class ProcessActionAssistance():
    def activateCard(self, card: Card, grid: Grid, assistingPlayer: int, 
                     assistingCard: Card, inputs: list[tuple[Resource, GridPosition]], 
                     outputs: list[tuple[Resource, GridPosition]], 
                     pollution: list[GridPosition]) -> bool:
        ...