# pylint: disable=too-many-instance-attributes, too-many-public-methods
from typing import List, Tuple, Any
import unittest
import json
from terra_futura.activation_pattern import ActivationPattern
from terra_futura.interfaces import InterfaceActivateGrid


class ActivateGridFake(InterfaceActivateGrid):
    activations: list[tuple[int, int]]

    def __init__(self) -> None:
        self.activations = []

    def set_activation_pattern(self, pattern: List[Tuple[int, int]]) -> None:
        self.activations = pattern


if __name__ == "__main__":
    unittest.main()


class TestActivationPattern(unittest.TestCase):
    def setUp(self) -> None:
        self.activate_grid: ActivateGridFake = ActivateGridFake()
        self.activation_pattern = ActivationPattern(
            self.activate_grid, [(0, 0), (-1, 1), (0, 0)])

    def check_state(self, activations: List[Tuple[int, int]], is_selected: bool) -> None:
        state: Any = json.loads(self.activation_pattern.state())
        self.assertEqual(state["selected"], is_selected)
        self.assertCountEqual(state["activations"], [
                              list(x) for x in activations])

    def test_activation_pattern_forwards_its_data_when_selected(self) -> None:
        test_pattern: list[tuple[int, int]] = [(0, 0), (0, 0), (-1, 1)]
        self.check_state(test_pattern, False)
        self.activation_pattern.select()
        self.check_state(test_pattern, True)
        self.assertCountEqual(self.activate_grid.activations, test_pattern)

    def test_pattern_cannot_be_activated_twice(self) -> None:
        self.activation_pattern.select()
        with self.assertRaises(AssertionError):
            self.activation_pattern.select()
