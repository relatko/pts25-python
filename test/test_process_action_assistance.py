import pytest

from typing import List, Optional, Dict
from terra_futura.simple_types import Resource
from terra_futura.simple_types import GridPosition
from terra_futura.process_action_assistance import ProcessActionAssistance
from terra_futura.card import Card
from terra_futura.interfaces import InterfaceGrid, InterfaceCard, Effect
from terra_futura.transformation_fixed import TransformationFixed

class DummyGrid(InterfaceGrid):
    def __init__(self, mapping: Dict[GridPosition, InterfaceCard]) -> None:
        self.mapping: Dict[GridPosition, InterfaceCard] = mapping

    def getCard(self, position) -> Optional[InterfaceCard]:
        return self.mapping.get(position)
    
    def canPutCard(self, coordinate: GridPosition)-> bool:
        return True

    def putCard(self, coordinate: GridPosition, card: InterfaceCard) -> bool:
        return True

    def canBeActivated(self, coordinate: GridPosition)-> bool:
        return True
        
    def setActivated(self, coordinate: GridPosition) -> None:
        pass

    def setActivationPattern(self, pattern: List[GridPosition]) -> None:
        pass
        
    def endTurn(self) -> None:
        pass

    def state(self) -> str:
        return ""
    
class AlwaysAssistanceEffect(Effect):
    def hasAssistance(self):
        return True
    def check(self, input, output, pollution):
        return True
    def state(self):
        return 'AlwaysAssistEffect'
    

class TransformationFixedAlwaysAssist(TransformationFixed):
    def hasAssistance(self):
        return True
    


class DummyPlayer:
    """
    Minimal dummy player wrapper for supplying a grid.
    """

    def __init__(self, grid: DummyGrid) -> None:
        self._grid = grid

    def getGrid(self) -> DummyGrid:
        return self._grid


def test_good_scenario_no_outputs() -> None:
    logic = ProcessActionAssistance()

    
    main_card = Card(pollutionSpacesL=1, upperEffect=AlwaysAssistanceEffect())
    main_card.putResources([Resource.RED, Resource.GREEN])
    main_grid = DummyGrid({GridPosition(1,1): main_card})
    main_pos = GridPosition(1,1)

    other_card = Card(pollutionSpacesL=1, upperEffect=TransformationFixedAlwaysAssist([Resource.GREEN, Resource.RED], [], 0))
    other_grid = DummyGrid({GridPosition(0,1): other_card})
    

    assistingPlayer = DummyPlayer(other_grid)
    inputs = [(Resource.GREEN, main_pos), (Resource.RED, main_pos)]
    outputs = []
    pollution = []

    result = logic.activateCard(
        main_card, main_grid,
        assistingPlayer, other_card,
        inputs, outputs, pollution
    )

    assert other_card.check(inputs, outputs, pollution)
    assert result is True


