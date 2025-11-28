from __future__ import annotations
import unittest

from typing import List, Optional
from terra_futura.simple_types import GridPosition
from terra_futura.interfaces import InterfaceGrid, InterfaceCard, InterfacePile
from terra_futura.move_card import MoveCard

class GridFake(InterfaceGrid):
    activations_received: List[GridPosition] 
    
    def __init__(self) -> None:
        self.activations_received = []

    def setActivationPattern(self, pattern: List[GridPosition]) -> None:
        self.activations_received = pattern

    def putCard(self, coordinate: GridPosition, card: InterfaceCard) -> None:
        ... 


class PileFake(InterfacePile):
    """Only gives the card information, does not change anything"""
    def getCard(self, index:int) ->Optional[InterfaceCard]:
        ...

    """Removes card from grid."""
    def takeCard(self, index: int) -> None:
        ...

    def removeLastCard(self) -> None:
        ...

    def state(self)-> str:
        ...


class TestMoveCard(unittest.TestCase):
    def setUp(self) ->None:
        pass