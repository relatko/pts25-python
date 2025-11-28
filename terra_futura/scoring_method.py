from .simple_types import Resource, Points
from typing import Optional

class ScoringMethod:
    resources: list[Resource]
    pointsPerCombination: Points
    calculatedTotal: Optional[Points]

    def __init__(self, resources: list[Resource], pointsPerCombination: Points):
        self.resources = resources.copy()
        self.pointsPerCombination = pointsPerCombination

    def selectThisMethodAndCalculate(self, resources: dict[Resource, int]):
        assert len(resources.keys()) == 8
        baseScores = [1, 1, 1, 5, 5, 6, 0, -1]
        calculatedTotal = 0
        for resource in Resource:
            calculatedTotal += baseScores[resource]*resources[resource]

        self.calculatedTotal = calculatedTotal

        assert self.pointsPerCombination > 0
        
        combinations = {}
        for resource in self.resources:
            combinations[resource] = combinations.get(resource, 0) + 1
        
        m = 9999
        for resource in combinations.keys():
            m = min(m, resources[resource]//combinations[resource])

        self.calculatedTotal += m*self.pointsPerCombination

    def state(self):
        return str(self.calculatedTotal)