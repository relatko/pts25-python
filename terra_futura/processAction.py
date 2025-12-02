from typing import List, Tuple, Any
from card import Card
from grid import Grid
from simple_types import GridPosition

Pair = Tuple[Any, GridPosition]

class ProcessAction:

    def activateCard(
        self,
        card: Card,
        grid: Grid,
        inputs: List[Pair],
        outputs: List[Pair],
        pollution: List[GridPosition]
    ) -> bool:
        if not card.can_activate():
            return False
        
        if not card.activate():
            return False
        
        return True