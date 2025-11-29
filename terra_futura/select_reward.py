from .card import Card
from .simple_types import Resource

class SelectReward():
    _player: int
    selection: list[Resource]

    @property
    def player(self) -> int:
        return self._player
    
    def setReward(self, player: int, card: Card, reward: list[Resource]):
        ...
    
    def canSelectReward(self, resource: Resource) -> bool:
        ...
    
    def selectReward(self, resource: Resource):
        ...

    def state(self) -> str:
        ...