import sys
import os
import random

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from terra_futura.simple_types import Resource, Points, GridPosition
from typing import Optional
from terra_futura.interfaces import InterfaceGrid

class ScoringMethod:
    resources: list[Resource]
    pointsPerCombination: Points
    calculatedTotal: Optional[Points]
    grid: InterfaceGrid

    def __init__(self, resources: list[Resource], pointsPerCombination: Points, grid: InterfaceGrid):
        self.resources = resources.copy()
        self.pointsPerCombination = pointsPerCombination
        self.calculatedTotal = None
        self.grid = grid

    def selectThisMethodAndCalculate(self) -> None:
        resources = {resource: 0 for resource in Resource}
        baseScores = {Resource.RED: 1,
                      Resource.GREEN: 1,
                      Resource.YELLOW: 1,
                      Resource.CONSTRUCTION: 5,
                      Resource.FOOD: 5,
                      Resource.GOODS: 6,
                      Resource.POLLUTION: 0,
                      Resource.MONEY: 0}
        calculatedTotal = 0

        for row in range(-2, 3):
            for col in range(-2, 3):
                card = self.grid.getCard(GridPosition(row, col))
                if card is not None:
                    if card.isActive():
                        for resource in card.resources:
                            resources[resource] += 1 
                    else:
                        calculatedTotal -= 1          


        for resource in Resource:
            calculatedTotal += baseScores[resource]*resources[resource]

        self.calculatedTotal = Points(calculatedTotal)

        assert self.pointsPerCombination.value >= 0
        
        combinations: dict[Resource, int] = {}
        for resource in self.resources:
            combinations[resource] = combinations.get(resource, 0) + 1
        
        m = 9999
        for resource in combinations.keys():
            m = min(m, resources[resource]//combinations[resource])

        self.calculatedTotal = Points(self.calculatedTotal.value + m*self.pointsPerCombination.value)

    def state(self) -> str:
        if self.calculatedTotal == None:
            return "Scoring method wasn't calculated"
        return str(self.calculatedTotal.value)