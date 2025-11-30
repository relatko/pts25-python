from .simple_types import Resource
from .interfaces import InterfaceSelectReward, InterfaceCard
from typing import List

class SelectReward(InterfaceSelectReward):
    _player: int
    selection: list[Resource]

    @property
    def player(self) -> int:
        return self._player
    
    def setReward(self, player: int, card: InterfaceCard, reward: List[Resource]) ->None:
        ...
    
    
    def canSelectReward(self, resource: Resource) -> bool:
        return False

    def selectReward(self, resource: Resource) -> None:
        ...

    def state(self)-> str:
        return ""