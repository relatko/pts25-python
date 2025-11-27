# pylint: disable=unused-argument, duplicate-code
from typing import List, Tuple, Optional
from terra_futura.simple_types import GridPosition, Resource


class InterfaceActivateGrid:
    def set_activation_pattern(self, pattern: List[Tuple[int, int]]) -> None:
        assert False

class InterfaceGrid:
    def putCard(self, coordinate : GridPosition, card: InterfaceCard) -> bool:
        assert False

class InterfaceMoveCard:
    """Interface for MoveCard"""
    def moveCard(pile: InterfacePile, gridCoordinate: GridPosition, grid: InterfaceGrid) ->bool:
        assert False
        
class InterfacePile:
    def getCard(index:int) ->Optional[InterfaceCard]:
        assert False

class InterfaceCard:
    def canGetResources(resources: List[Resource]) -> bool:
        assert False

    # treba implementovať zvyšok ...