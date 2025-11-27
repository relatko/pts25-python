# pylint: disable=unused-argument, duplicate-code
from typing import List, Tuple, Optional, Protocol
from terra_futura.simple_types import *

# Zostalo z pôvodného...
class InterfaceActivateGrid(Protocol):
    def set_activation_pattern(self, pattern: List[Tuple[int, int]]) -> None:
        ...

# Card
class InterfaceCard(Protocol):
    def canGetResources(self, resources: List[Resource]) -> bool:
        ...

# Pile
class InterfacePile(Protocol):
    def getCard(self, index:int) ->Optional[InterfaceCard]:
        ...

# Grid
class InterfaceGrid(Protocol):
    def putCard(self, coordinate : GridPosition, card: InterfaceCard) -> None:
        ...

# MoveCard
class InterfaceMoveCard(Protocol):
    """Interface for MoveCard"""
    def moveCard(self, pile: InterfacePile, gridCoordinate: GridPosition, grid: InterfaceGrid) ->bool:
        ...
        

    # treba implementovať zvyšok ...