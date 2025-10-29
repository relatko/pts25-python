from __future__ import annotations
import json
from typing import List, Tuple, Any
from terra_futura.interfaces import InterfaceActivateGrid


class ActivationPattern:
    _pattern: list[tuple[int, int]]
    _selected: bool
    _grid: InterfaceActivateGrid

    def __init__(self, grid: InterfaceActivateGrid, pattern: List[Tuple[int, int]]):
        self._grid = grid
        self._pattern = pattern.copy()
        self._selected = False

    def select(self) -> None:
        assert self._selected is False
        self._grid.set_activation_pattern(self._pattern)
        self._selected = True

    def is_selected(self) -> bool:
        return self._selected

    def state(self) -> str:
        state: Any = {
            "activations": self._pattern,
            "selected": self._selected,
        }
        return json.dumps(state)
