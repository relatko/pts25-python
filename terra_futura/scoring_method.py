import sys
import os
import random

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from terra_futura.simple_types import Resource, Points
from typing import Optional

class ScoringMethod:
    resources: list[Resource]
    pointsPerCombination: Points
    calculatedTotal: Optional[Points]

    def __init__(self, resources: list[Resource], pointsPerCombination: Points):
        self.resources = resources.copy()
        self.pointsPerCombination = pointsPerCombination

    def selectThisMethodAndCalculate(self, resources: dict[Resource, int]) -> None:
        assert len(resources.keys()) == 8
        baseScores = [1, 1, 1, 5, 5, 6, 0, -1]
        calculatedTotal = 0
        for resource in Resource:
            calculatedTotal += baseScores[resource.value-1]*resources[resource]

        self.calculatedTotal = Points(calculatedTotal)

        assert self.pointsPerCombination.value > 0
        
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