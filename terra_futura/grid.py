from terra_futura.interfaces import InterfaceGrid
from typing import Optional
from terra_futura.simple_types import *
from .card import Card

class Grid (InterfaceGrid):
    def __init__(self):
        pass
    
    def getCard(self, coordinate: GridPosition) -> Optional[Card]:
        ...

    def endTurn(self) -> None:
        ...

    def setActivationPattern(self, pattern: list[GridPosition]):
        ...

    def state(self) -> str:
        ...