import unittest
import json
from card import Card, Deck, StartingCard
from select_reward import Resource


class TestCard(unittest.TestCase):
    def setUp(self) -> None:
        self.level_i_card = Card(
            name="TestLevelI",
            level=Deck.I,
            output=Resource.GREEN,
            pollution=0,
            pollution_spaces=1,
            has_assistance=False
        )
        self.level_ii_card = Card(
            name="TestLevelII",
            level=Deck.II,
            input=[Resource.GREEN, Resource.RED],
            output=Resource.GEAR,
            pollution=1,
            pollution_spaces=2,
            has_assistance=True
        )

    def test_initialization_level_i(self) -> None:
        self.assertEqual(self.level_i_card.name, "TestLevelI")
        self.assertEqual(self.level_i_card.level, Deck.I)
        self.assertEqual(self.level_i_card.input, [])
        self.assertEqual(self.level_i_card.output, Resource.GREEN)
        self.assertEqual(self.level_i_card.pollution, 0)
        self.assertEqual(self.level_i_card.pollution_spaces, 1)
        self.assertFalse(self.level_i_card.has_assistance_atr)
        self.assertEqual(self.level_i_card.resources, [])
        self.assertEqual(self.level_i_card.pollution_count, 0)
        self.assertTrue(self.level_i_card.active)

    def test_initialization_level_ii(self) -> None:
        self.assertEqual(self.level_ii_card.name, "TestLevelII")
        self.assertEqual(self.level_ii_card.level, Deck.II)
        self.assertEqual(self.level_ii_card.input, [Resource.GREEN, Resource.RED])
        self.assertEqual(self.level_ii_card.output, Resource.GEAR)
        self.assertEqual(self.level_ii_card.pollution, 1)
        self.assertEqual(self.level_ii_card.pollution_spaces, 2)
        self.assertTrue(self.level_ii_card.has_assistance_atr)
        self.assertEqual(self.level_ii_card.resources, [])
        self.assertEqual(self.level_ii_card.pollution_count, 0)
        self.assertTrue(self.level_ii_card.active)

    def test_can_activate_level_i(self) -> None:
        self.assertTrue(self.level_i_card.can_activate())
        self.level_i_card.active = False
        self.assertFalse(self.level_i_card.can_activate())

    def test_can_activate_level_ii_with_resources(self) -> None:
        self.level_ii_card.put_resources([Resource.GREEN, Resource.RED])
        self.assertTrue(self.level_ii_card.can_activate())

    def test_can_activate_level_ii_without_resources(self) -> None:
        self.assertFalse(self.level_ii_card.can_activate())
        self.level_ii_card.put_resources([Resource.GREEN])
        self.assertFalse(self.level_ii_card.can_activate())

    def test_activate_level_i_success(self) -> None:
        result = self.level_i_card.activate()
        self.assertTrue(result)
        self.assertEqual(self.level_i_card.resources, [Resource.GREEN])
        self.assertEqual(self.level_i_card.pollution_count, 0)

    def test_activate_level_ii_success(self) -> None:
        self.level_ii_card.put_resources([Resource.GREEN, Resource.RED])
        result = self.level_ii_card.activate()
        self.assertTrue(result)
        self.assertEqual(self.level_ii_card.resources, [Resource.GEAR])
        self.assertEqual(self.level_ii_card.pollution_count, 1)

    def test_activate_level_ii_failure(self) -> None:
        result = self.level_ii_card.activate()
        self.assertFalse(result)
        self.assertEqual(self.level_ii_card.resources, [])
        self.assertEqual(self.level_ii_card.pollution_count, 0)

    def test_activate_with_pollution(self) -> None:
        polluting_card = Card(
            name="PollutingFactory",
            level=Deck.II,
            input=[Resource.GREEN],
            output=Resource.BULB,
            pollution=2,
            pollution_spaces=1
        )
        polluting_card.put_resources([Resource.GREEN])
        result = polluting_card.activate()
        self.assertTrue(result)
        self.assertEqual(polluting_card.pollution_count, 2)
        self.assertFalse(polluting_card.active)

    def test_can_get_resources(self) -> None:
        self.level_ii_card.put_resources([Resource.GREEN, Resource.RED, Resource.YELLOW])
        self.assertTrue(self.level_ii_card.can_get_resources([Resource.GREEN]))
        self.assertTrue(self.level_ii_card.can_get_resources([Resource.GREEN, Resource.RED]))
        self.assertFalse(self.level_ii_card.can_get_resources([Resource.BULB]))
        self.assertFalse(self.level_ii_card.can_get_resources([Resource.GREEN, Resource.GREEN]))

    def test_get_resources(self) -> None:
        self.level_ii_card.put_resources([Resource.GREEN, Resource.RED, Resource.YELLOW])
        result = self.level_ii_card.get_resources([Resource.GREEN, Resource.RED])
        self.assertTrue(result)
        self.assertEqual(self.level_ii_card.resources, [Resource.YELLOW])

    def test_put_resources(self) -> None:
        result = self.level_ii_card.put_resources([Resource.BULB, Resource.GEAR])
        self.assertTrue(result)
        self.assertEqual(self.level_ii_card.resources, [Resource.BULB, Resource.GEAR])

    def test_add_pollution_within_limits(self) -> None:
        result = self.level_ii_card.add_pollution(1)
        self.assertTrue(result)
        self.assertEqual(self.level_ii_card.pollution_count, 1)
        self.assertTrue(self.level_ii_card.active)

    def test_add_pollution_exceed_limits(self) -> None:
        result = self.level_ii_card.add_pollution(3)
        self.assertFalse(result)
        self.assertEqual(self.level_ii_card.pollution_count, 3)
        self.assertFalse(self.level_ii_card.active)

    def test_remove_pollution(self) -> None:
        self.level_ii_card.add_pollution(2)
        result = self.level_ii_card.remove_pollution(1)
        self.assertTrue(result)
        self.assertEqual(self.level_ii_card.pollution_count, 1)
        self.assertTrue(self.level_ii_card.active)

    def test_has_assistance(self) -> None:
        self.assertFalse(self.level_i_card.has_assistance())
        self.assertTrue(self.level_ii_card.has_assistance())

    def test_state_method_level_i(self) -> None:
        state = self.level_i_card.state()
        state_dict = json.loads(state)
        self.assertEqual(state_dict["name"], "TestLevelI")
        self.assertEqual(state_dict["level"], "I")
        self.assertEqual(state_dict["input"], [])
        self.assertEqual(state_dict["output"], "Green")
        self.assertEqual(state_dict["pollution"], 0)
        self.assertEqual(state_dict["pollution_spaces"], 1)
        self.assertEqual(state_dict["has_assistance"], False)
        self.assertEqual(state_dict["active"], True)

    def test_state_method_level_ii(self) -> None:
        state = self.level_ii_card.state()
        state_dict = json.loads(state)
        self.assertEqual(state_dict["name"], "TestLevelII")
        self.assertEqual(state_dict["level"], "II")
        self.assertEqual(state_dict["input"], ["Green", "Red"])
        self.assertEqual(state_dict["output"], "Gear")
        self.assertEqual(state_dict["pollution"], 1)
        self.assertEqual(state_dict["pollution_spaces"], 2)
        self.assertEqual(state_dict["has_assistance"], True)
        self.assertEqual(state_dict["active"], True)

    def test_repr_method_level_i(self) -> None:
        repr_str = repr(self.level_i_card)
        self.assertIn("TestLevelI", repr_str)
        self.assertIn("level=I", repr_str)
        self.assertIn("output=Resource.GREEN", repr_str)

    def test_repr_method_level_ii(self) -> None:
        repr_str = repr(self.level_ii_card)
        self.assertIn("TestLevelII", repr_str)
        self.assertIn("level=II", repr_str)
        self.assertIn("input=[<Resource.GREEN: 'Green'>, <Resource.RED: 'Red'>]→output=Resource.GEAR", repr_str)

class TestStartingCard(unittest.TestCase):
    def test_starting_card_initialization(self) -> None:
        starting_card = StartingCard()
        self.assertEqual(starting_card.name, "StartingCard")
        self.assertEqual(starting_card.level, Deck.I)
        self.assertEqual(starting_card.output, Resource.GREEN)
        self.assertEqual(starting_card.pollution, 0)
        self.assertEqual(starting_card.pollution_spaces, 1)
        self.assertTrue(starting_card.has_assistance_atr)

    def test_starting_card_activation(self) -> None:
        starting_card = StartingCard()
        result = starting_card.activate()
        self.assertTrue(result)
        self.assertEqual(starting_card.resources, [Resource.GREEN])

    def test_starting_card_assistance(self) -> None:
        starting_card = StartingCard()
        self.assertTrue(starting_card.has_assistance())

class TestCardEdgeCases(unittest.TestCase):
    def test_level_ii_card_with_empty_input(self) -> None:
        card = Card(name="Producer", level=Deck.II, input=[], output=Resource.GREEN, pollution=0)
        self.assertTrue(card.can_activate())
        result = card.activate()
        self.assertTrue(result)
        self.assertEqual(card.resources, [Resource.GREEN])

    def test_zero_pollution_card(self) -> None:
        card = Card(name="CleanCard", level=Deck.I, output=Resource.GREEN, pollution=0, pollution_spaces=0)
        result = card.activate()
        self.assertTrue(result)
        self.assertEqual(card.resources, [Resource.GREEN])

    def test_inactive_card_operations(self) -> None:
        card = Card(name="InactiveTest", level=Deck.I, output=Resource.GREEN, pollution=0)
        card.active = False
        self.assertFalse(card.can_activate())
        self.assertFalse(card.activate())
        self.assertFalse(card.put_resources([Resource.GREEN]))

    def test_complex_resource_scenario(self) -> None:
        factory = Card(name="Factory", level=Deck.II, input=[Resource.GREEN], output=Resource.BULB, pollution=1, pollution_spaces=2)
        factory.put_resources([Resource.GREEN])
        result1 = factory.activate()
        self.assertTrue(result1)
        self.assertEqual(factory.resources, [Resource.BULB])
        self.assertEqual(factory.pollution_count, 1)
        factory.put_resources([Resource.GREEN])
        result2 = factory.activate()
        self.assertTrue(result2)
        self.assertEqual(factory.resources, [Resource.BULB, Resource.BULB])
        self.assertEqual(factory.pollution_count, 2)
        factory.put_resources([Resource.GREEN])
        result3 = factory.activate()
        self.assertTrue(result3)
        self.assertEqual(factory.pollution_count, 3)
        self.assertFalse(factory.active)

if __name__ == "__main__":
    unittest.main()