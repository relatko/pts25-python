# pylint: disable=unused-argument, duplicate-code
from __future__ import annotations
from typing import List , Optional , Tuple


class InterfaceActivateGrid:
    def set_activation_pattern(self, pattern: List[Tuple[int, int]]) -> None:
        assert False
        
class TerraFuturaObserverInterface:
    def notify(self, gameState: str) -> None:
        assert False
