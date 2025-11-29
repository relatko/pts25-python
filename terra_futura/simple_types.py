from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Union


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
        return "("+str(self._x)+","+str(self._y)+")"

class Resource(Enum):
    GREEN = 1
    RED = 2
    YELLOW = 3
    BULB = 4
    GEAR = 5
    CAR =6
    MONEY = 7
    POLLUTION = 8

    def __str__(self) -> str:
        return self.name

class Deck(Enum):
    I = 1
    II = 2

class CardSource:
    _deck: Deck
    _index: int

    def __init__(self, deck: Deck, index : int):
        assert index >= 0, "Index CardSource init less 0"
        self._deck = deck
        self._index = index

    @property
    def deck(self) -> Deck:
        return self._deck

    @deck.setter
    def deck(self,value: Deck) -> None:
        self._deck = value

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self,value: int) -> None:
        assert value >= 0, "Index CardSource less 0 setter"
        self._index = value

class GameState(Enum):
    TakeCardNoCardDiscarded = "TakeCardNoCardDiscarded"
    TakeCardCardDiscarded = "TakeCardCardDiscarded"
    ActivateCard = "ActivateCard"
    SelectReward = "SelectReward"
    SelectActivationPattern = "SelectActivationPattern"
    SelectScoringMethod = "SelectScoringMethod"
    Finish = "Finish"

@dataclass
class Points:
    value: int

    def __str__(self) -> str:
        return f"{self.value} VP"

    def __add__(self, other: Union[Points, int]) -> Points:
        if isinstance(other, Points):
            return Points(self.value + other.value)
        return Points(self.value + other)

    def __sub__(self, other: Union[Points, int]) -> Points:
        if isinstance(other, Points):
            return Points(self.value - other.value)
        return Points(self.value - other)
