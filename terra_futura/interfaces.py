# pylint: disable=unused-argument, duplicate-code
from typing import List, Tuple, Optional, Protocol
from terra_futura.simple_types import *

# Zostalo z pôvodného...
class InterfaceActivateGrid(Protocol):
    def set_activation_pattern(self, pattern: List[Tuple[int, int]]) -> None:
        ...

# Card
class InterfaceCard(Protocol):
    def canGetResources(self, resources: List[Resource]) -> bool:
        ...

# Pile
class InterfacePile(Protocol):
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

# Grid
class InterfaceGrid(Protocol):
    def getCard(self, coordinate: GridPosition)-> Optional[InterfaceCard]:
        ...

    def canPutCard(self, coordinate: GridPosition)-> bool:
        ...

    def putCard(self, coordinate: GridPosition, card: InterfaceCard) -> bool:
        ...

    def canBeActivated(self, coordinate: GridPosition)-> bool:
        ...
        
    def setActivated(self, coordinate: GridPosition) -> None:
        ...

    def setActivationPattern(self, pattern: List[GridPosition]) -> None:
        ...
    def endTurn(self) -> None:
        ...

    def state(self) -> None:
        ...


# MoveCard
class InterfaceMoveCard(Protocol):
    """IMPORTANT! Added cardIndex argument"""
    def moveCard(self, pile: InterfacePile,cardIndex: int, gridCoordinate: GridPosition, grid: InterfaceGrid) ->bool:
        ...
        

    # treba implementovať zvyšok ...

class TerraFuturaInterface(Protocol):
    def takeCard(self, playerId: int, source: CardSource, cardIndex: int, destination: GridPosition) -> bool:
        ...
    
    def discardLastCardFromDeck(self, playerId: int, deck: Deck) -> bool:
        ...

    def activateCard(self, playerId: int, card: GridPosition, 
                     inputs: List[tuple[Resource, GridPosition]], 
                     outputs: List[tuple[Resource, GridPosition]],
                     pollution: List[GridPosition], 
                     otherPlayerId: Optional[int], otherCard: Optional[GridPosition]) -> None:
        ...
    
    def selectReward(self, playerId: int, resource: Resource) -> None:
        ...

    def turnFinished(self, playerId: int) -> bool:
        ...
    
    def selectActivationPattern(self, playerId: int, card: int) -> bool:
        ...
    
    def selectScoring(self, playerId: int, card: int) -> bool:
        ...

class TerraFuturaObserverInterface(Protocol):
    def notify(self, state: GameState) -> None:
        ...

class GameObserverInterface(Protocol):
    def notifyAll(self, newState: dict[int, str]) -> None:
        ...

