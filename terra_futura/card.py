from typing import List, Optional
from enumeration_classes import Deck, Resource
import json

class Card:
    def __init__(self, name: str, level: Deck, output: Resource, input: Optional[List[Resource]] = None, pollution: int = 0,
                 pollution_spaces: int = 0, has_assistance: bool = False):
        self.name = name
        self.level = level
        self.input = input or []
        self.output = output
        self.pollution = pollution
        self.pollution_spaces = pollution_spaces
        self.has_assistance_atr = has_assistance
        self.resources: List[Resource] = []
        self.pollution_count: int = 0
        self.active: bool = True

    def can_activate(self) -> bool:
        if not self.active:
            return False
        if self.level == Deck.I:
            return True
        if self.level == Deck.II:
            return self.can_get_resources(self.input)
        return False

    def activate(self) -> bool:
        if not self.can_activate():
            return False
        if self.level == Deck.II and self.input:
            if not self.get_resources(self.input):
                return False
        self.put_resources([self.output])
        if self.pollution > 0:
            self.add_pollution(self.pollution)
        return True

    def can_get_resources(self, resources: List[Resource]) -> bool:
        available_resources = self.resources.copy()
        for resource in resources:
            if resource in available_resources:
                available_resources.remove(resource)
            else:
                return False
        return True

    def get_resources(self, resources: List[Resource]) -> bool:
        if not self.can_get_resources(resources):
            return False
        for resource in resources:
            self.resources.remove(resource)
        return True

    def can_put_resources(self, resources: List[Resource]) -> bool:
        return self.active

    def put_resources(self, resources: List[Resource]) -> bool:
        if not self.can_put_resources(resources):
            return False
        self.resources.extend(resources)
        return True

    def add_pollution(self, amount: int = 1) -> bool:
        if self.pollution_count + amount <= self.pollution_spaces:
            self.pollution_count += amount
            return True
        else:
            self.active = False
            self.pollution_count += amount
            return False

    def remove_pollution(self, amount: int = 1) -> bool:
        if self.pollution_count >= amount:
            self.pollution_count -= amount
            if self.pollution_count <= self.pollution_spaces:
                self.active = True
            return True
        return False

    def has_assistance(self) -> bool:
        return self.has_assistance_atr

    def state(self) -> str:
        state_info = {
            "name": self.name,
            "level": self.level.value,
            "input": [resource.value for resource in self.input],
            "output": self.output.value,
            "pollution": self.pollution,
            "pollution_spaces": self.pollution_spaces,
            "pollution_count": self.pollution_count,
            "has_assistance": self.has_assistance_atr,
            "active": self.active,
            "resources": [resource.value for resource in self.resources]
        }
        return json.dumps(state_info)

    def __repr__(self) -> str:
        if self.level == Deck.I:
            return f"Card(name={self.name}, level=I, output={self.output}, pollution={self.pollution})"
        else:
            return f"Card(name={self.name}, level=II, input={self.input}→output={self.output}, pollution={self.pollution})"

class StartingCard(Card):
    def __init__(self):
        super().__init__(name="StartingCard", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=1, has_assistance=True)