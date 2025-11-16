from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from collections import Counter

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
    POLUTION = 8

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
    TAKE_CARD_NO_CARD_DISCARDED = 1
    TAKE_CARD_CARD_DISCARDED = 2
    ACTIVATE_CARD = 3
    SELECT_REWARD = 4
    SELECT_ACTIVATION_PATTERN = 5
    SELECT_SCORING_METHOD = 6
    FINISH = 7


@dataclass
class Points:
    value: int

    def __str__(self) -> str:
        return f"{self.value} VP"

    def __add__(self, other):
        if isinstance(other, Points):
            return Points(self.value + other.value)
        return Points(self.value + other)

    def __sub__(self, other):
        if isinstance(other, Points):
            return Points(self.value - other.value)
        return Points(self.value - other)


class ScoringMethod:

    def __init__(self, resources: List[Resource], points_per_combination: Points):

        self.resources: List[Resource] = resources
        self.points_per_combination: Points = points_per_combination
        self.calculated_total: Optional[Points] = None
        self.selected: bool = False

    def select_this_method_and_calculate(self, available_resources: List[Resource]) -> Points:
        self.selected = True

        required = Counter(self.resources)

        available = Counter(r for r in available_resources
                            if r not in [Resource.MONEY, Resource.POLUTION])

        if not required:
            num_complete_sets = 0
        else:

            num_complete_sets = min(
                available.get(resource, 0) // required[resource]
                for resource in required
            )

        total_points = Points(num_complete_sets * self.points_per_combination.value)
        self.calculated_total = total_points

        return total_points

    def state(self) -> str:

        resource_names = [r.name for r in self.resources]
        total_str = str(self.calculated_total) if self.calculated_total else "Not calculated"

        return (f"ScoringMethod["
                f"resources={resource_names}, "
                f"points={self.points_per_combination}, "
                f"selected={self.selected}, "
                f"total={total_str}]")