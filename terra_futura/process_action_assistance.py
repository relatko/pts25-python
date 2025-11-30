from .simple_types import Resource, GridPosition
from .interfaces import ProcessActionAssistanceInterface, InterfaceCard, InterfaceGrid

class ProcessActionAssistance(ProcessActionAssistanceInterface):
    def activateCard(self, card: InterfaceCard, grid: InterfaceGrid, assistingPlayer: int, 
                     assistingCard: InterfaceCard, inputs: list[tuple[Resource, GridPosition]], 
                     outputs: list[tuple[Resource, GridPosition]], 
                     pollution: list[GridPosition]) -> bool:
        return False