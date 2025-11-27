from __future__ import annotations
import json
from typing import List, Tuple, Any
from terra_futura.simple_types import GridPosition
from terra_futura.interfaces import InterfaceMoveCard, InterfaceGrid, InterfacePile

class MoveCard(InterfaceMoveCard):
    def __init__(self):
        pass

    def moveCard(pile:InterfacePile, gridCoordinate: GridPosition, grid: InterfaceGrid) ->bool:
        card = pile.getCard()
        # implementacia ...