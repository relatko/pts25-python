from .card import Card
from .grid import Grid
from .simple_types import Resource, GridPosition

class ProcessAction():
    def activateCard(self, card: Card, grid: Grid, 
                     inputs: list[tuple[Resource, GridPosition]], 
                     outputs: list[tuple[Resource, GridPosition]], 
                     pollution: list[GridPosition]) -> bool:
        return False
