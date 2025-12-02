from __future__ import annotations

from typing import Dict, List, Optional
import json

from resource import Resource
from card import Card


class ScoringMethod:
    def __init__(
        self,
        resources: List[Resource],
        points_per_combination: int,
        resource_values: Dict[Resource, int],
    ) -> None:
        self.resources = resources.copy()
        self.points_per_combination = points_per_combination
        self.resource_values = dict(resource_values)
        self.calculated_total: Optional[int] = None
        self._last_breakdown: Optional[Dict] = None

    def selectThisMethodAndCalculate(self, cards: List[Card]) -> int:
        resource_counts: Dict[Resource, int] = {}
        for c in cards:
            if not getattr(c, "active", True):
                continue
            for res in getattr(c, "resources", []):
                resource_counts[res] = resource_counts.get(res, 0) + 1

        required: Dict[Resource, int] = {}
        for r in self.resources:
            required[r] = required.get(r, 0) + 1

        if required:
            sets_possible = min(
                (resource_counts.get(r, 0) // cnt) for r, cnt in required.items()
            )
        else:
            sets_possible = 0

        points_from_sets = sets_possible * self.points_per_combination

        resource_points = 0
        for r, cnt in resource_counts.items():
            value = self.resource_values.get(r, 0)
            resource_points += value * cnt

        pollution_penalty = 0
        for c in cards:
            poll = getattr(c, "pollution_count", 0)
            if poll >= 1:
                pollution_penalty += 1

        total = points_from_sets + resource_points - pollution_penalty

        self.calculated_total = total
        self._last_breakdown = {
            "sets": sets_possible,
            "points_from_sets": points_from_sets,
            "resource_points": resource_points,
            "pollution_penalty": pollution_penalty,
            "total": total,
        }
        return total

    def state(self) -> str:
        if self._last_breakdown is None:
            info = {
                "pattern": [r.value for r in self.resources],
                "points_per_combination": self.points_per_combination,
                "resource_values": {r.value: v for r, v in self.resource_values.items()},
                "calculated_total": None,
            }
        else:
            info = {**self._last_breakdown}
            info["pattern"] = [r.value for r in self.resources]
            info["points_per_combination"] = self.points_per_combination
            info["resource_values"] = {r.value: v for r, v in self.resource_values.items()}

        return json.dumps(info)


__all__ = ["ScoringMethod"]
