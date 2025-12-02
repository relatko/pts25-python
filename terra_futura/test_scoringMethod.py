import unittest
from select_reward import Resource
from scoringMethod import ScoringMethod
from card import Card, Deck


class TestScoringMethod(unittest.TestCase):
    def test_sets_resources_and_pollution(self) -> None:
        """Test set scoring with resource values and pollution penalty."""
        c1 = Card(name="C1", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=1)
        c2 = Card(name="C2", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=1)
        c3 = Card(name="C3", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=1)
        c1.resources = [Resource.GREEN, Resource.GREEN, Resource.RED]
        c1.pollution_count = 1
        c2.resources = [Resource.GREEN]
        c3.resources = [Resource.GREEN]
        c3.active = False
        pattern = [Resource.GREEN, Resource.GREEN, Resource.RED]
        values = {Resource.GREEN: 2, Resource.RED: 3, Resource.BULB: 5, Resource.GEAR: 4}
        sm = ScoringMethod(resources=pattern, points_per_combination=10, resource_values=values)
        total = sm.selectThisMethodAndCalculate([c1, c2, c3])
        self.assertEqual(total, 18)

    def test_multiple_sets_and_values(self) -> None:
        """Test multiple sets with resource scoring."""
        a = Card(name="A", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=1)
        b = Card(name="B", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=1)
        a.resources = [Resource.GREEN, Resource.GREEN]
        b.resources = [Resource.GREEN, Resource.GREEN]
        pattern = [Resource.GREEN, Resource.GREEN]
        values = {Resource.GREEN: 1}
        sm = ScoringMethod(resources=pattern, points_per_combination=5, resource_values=values)
        total = sm.selectThisMethodAndCalculate([a, b])
        self.assertEqual(total, 14)

    def test_money_has_no_value(self) -> None:
        """Test that money contributes 0 VP."""
        c = Card(name="C", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=1)
        c.resources = [Resource.GREEN, Resource.MONEY]
        pattern = [Resource.GREEN]
        values = {Resource.GREEN: 2, Resource.MONEY: 0}
        sm = ScoringMethod(resources=pattern, points_per_combination=5, resource_values=values)
        total = sm.selectThisMethodAndCalculate([c])
        self.assertEqual(total, 7)

    def test_inactive_cards_ignored(self) -> None:
        """Test that inactive cards are not scored."""
        c = Card(name="C", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=1)
        c.resources = [Resource.GREEN, Resource.RED]
        c.active = False
        pattern = [Resource.GREEN, Resource.RED]
        values = {Resource.GREEN: 2, Resource.RED: 3}
        sm = ScoringMethod(resources=pattern, points_per_combination=10, resource_values=values)
        total = sm.selectThisMethodAndCalculate([c])
        self.assertEqual(total, 0)

    def test_state_json(self) -> None:
        """Test that state() returns valid JSON with total."""
        c = Card(name="C", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=1)
        c.resources = [Resource.GREEN, Resource.RED]
        pattern = [Resource.GREEN, Resource.RED]
        values = {Resource.GREEN: 2, Resource.RED: 3}
        sm = ScoringMethod(resources=pattern, points_per_combination=10, resource_values=values)
        sm.selectThisMethodAndCalculate([c])
        state = sm.state()
        self.assertIn('"total":', state)


if __name__ == "__main__":
    unittest.main()

