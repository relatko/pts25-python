from .card import Card
from .simple_types import Resource

class SelectReward():
    def setReward(self, player: int, card: Card, reward: list[Resource]):
        ...
    
    def canSelectReward(self, resource: Resource) -> bool:
        ...
    
    def selectReward(self, resource: Resource):
        ...

    def state(self) -> str:
        ...