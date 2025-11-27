from __future__ import annotations
from enum import Enum, auto

class GridPosition:
    _x: int
    _y: int

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __str__(self) -> str:
        return f"({self._x},{self._y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GridPosition):
            return False
        return self._x == other._x and self._y == other._y

    def __hash__(self) -> int:
        return hash((self._x, self._y))


class Resource(Enum):
    YELLOW = auto()  # Raw material
    RED = auto()     # Raw material
    GREEN = auto()   # Raw material
    GOODS = auto()   # Product
    FOOD = auto()    # Product
    CONSTRUCTION = auto()  # Product
    MONEY = auto()
    POLLUTION = auto()  # Not a resource, but tracked


class Deck(Enum):
    LEVEL_I = auto()
    LEVEL_II = auto()


class CardSource(Enum):
    DISPLAY_LEVEL_I_0 = auto()
    DISPLAY_LEVEL_I_1 = auto()
    DISPLAY_LEVEL_I_2 = auto()
    DISPLAY_LEVEL_I_3 = auto()
    DISPLAY_LEVEL_II_0 = auto()
    DISPLAY_LEVEL_II_1 = auto()
    DISPLAY_LEVEL_II_2 = auto()
    DISPLAY_LEVEL_II_3 = auto()
    DECK_LEVEL_I = auto()
    DECK_LEVEL_II = auto()

class Points:
    _amount: int

    def __init__(self, amount: int):
        self._amount = amount

    @property
    def amount(self) -> int:
        return self._amount
    
    
