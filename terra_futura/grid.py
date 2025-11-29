from terra_futura.interfaces import InterfaceGrid, InterfaceCard
from typing import Optional, List
from terra_futura.simple_types import *
from .card import Card

class Grid (InterfaceGrid):
    def __init__(self) ->None:
        pass
    
    def getCard(self, coordinate: GridPosition)-> Optional[InterfaceCard]:
        ...

    def canPutCard(self, coordinate: GridPosition)-> bool:
        return False

    def putCard(self, coordinate: GridPosition, card: InterfaceCard) -> bool:
        return False

    def canBeActivated(self, coordinate: GridPosition)-> bool:
        return False
        
    def setActivated(self, coordinate: GridPosition) -> None:
        ...

    def setActivationPattern(self, pattern: List[GridPosition]) -> None:
        ...
        
    def endTurn(self) -> None:
        ...

    def state(self) -> str:
        return ""