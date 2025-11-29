from .card import Card
from .interfaces import InterfaceCard, InterfaceSelectReward
from typing import List
from .simple_types import Resource

class SelectReward(InterfaceSelectReward):
    def setReward(self, player: int, card: InterfaceCard, reward: List[Resource]) ->None:
        ...
    
    def canSelectReward(self, resource: Resource) -> bool:
        return False

    def selectReward(self, resource: Resource) -> None:
        ...

    def state(self)-> str:
        return ""