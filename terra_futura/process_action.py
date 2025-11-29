from .simple_types import Resource, GridPosition
from .interfaces import ProcessActionInterface, InterfaceCard, InterfaceGrid

class ProcessAction(ProcessActionInterface):
    def activateCard(self, card: InterfaceCard, grid: InterfaceGrid, 
                     inputs: list[tuple[Resource, GridPosition]], 
                     outputs: list[tuple[Resource, GridPosition]], 
                     pollution: list[GridPosition]) -> bool:
        return False
