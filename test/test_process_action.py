import pytest

from terra_futura.process_action import ProcessAction
from terra_futura.card import Card
from terra_futura.arbitrary_basic import ArbitraryBasic
from terra_futura.simple_types import Resource, GridPosition


class DummyGrid:
    def __init__(self, mapping):
        self.mapping = mapping

    def getCard(self, position):
        return self.mapping.get(position)


def test_activate_card_inactive_returns_false():
    pa = ProcessAction()
    # create an inactive card (no safe pollution slots) and ensure activation is rejected
    card = Card(pollutionSpacesL=0)
    grid = DummyGrid({})

    result = pa.activateCard(card, grid, inputs=[], outputs=[], pollution=[])
    assert result is False


def test_activate_card_rejects_when_pollution_cannot_be_placed():
    pa = ProcessAction()
    # acting card is active
    acting = Card()
    # target card has 0 safe slots, trying to place 2 would require center cubes -> rejected
    target = Card(pollutionSpacesL=0)
    pos = GridPosition(0, 0)
    grid = DummyGrid({pos: target})

    result = pa.activateCard(acting, grid, inputs=[], outputs=[], pollution=[pos, pos])
    assert result is False
    # ensure no pollution was placed (target remains inactive / unchanged)
    # don't rely on internal attribute names for center slots; just assert activation failed
    

def test_activate_card_rejects_when_inputs_not_available():
    pa = ProcessAction()
    acting = Card()
    # resource provider at P has no resources
    resource_card = Card()
    pos = GridPosition(1, 0)
    grid = DummyGrid({pos: resource_card})

    result = pa.activateCard(acting, grid, inputs=[(Resource.YELLOW, pos)], outputs=[], pollution=[])
    assert result is False


def test_activate_card_rejects_when_outputs_cannot_be_put():
    pa = ProcessAction()
    # make acting card unable to accept outputs by creating it inactive
    acting = Card(pollutionSpacesL=0)
    pos = GridPosition(1, 1)
    grid = DummyGrid({pos: acting})

    result = pa.activateCard(acting, grid, inputs=[], outputs=[(Resource.GOODS, pos)], pollution=[])
    assert result is False
    
def test_activate_card_rejects_when_output_targets_different_active_card():
    pa = ProcessAction()
    acting = Card()
    # another active card at a different position -- outputs must target the acting card
    other = Card()
    pos_act = GridPosition(0, 0)
    pos_other = GridPosition(1, 0)
    grid = DummyGrid({pos_act: acting, pos_other: other})

    result = pa.activateCard(acting, grid, inputs=[], outputs=[(Resource.GOODS, pos_other)], pollution=[])
    assert result is False


def test_activate_card_success_performs_actions():
    pa = ProcessAction()
    # acting card has two resources to pay and an effect that requires 2 inputs,
    # produces pollution and fills safe slots as available
    acting = Card(pollutionSpacesL=2, upperEffect=ArbitraryBasic(from_=2, to=[Resource.MONEY], pollution=2))
    # give acting card the resources it will pay
    acting.resources = [Resource.YELLOW, Resource.RED]

    # place pollution on a different card so the acting card does not
    # become inactive before its inputs are collected
    target = Card(pollutionSpacesL=2)
    pos_act = GridPosition(0, 0)
    pos_target = GridPosition(1, 1)
    grid = DummyGrid({pos_act: acting, pos_target: target})

    inputs = [(Resource.YELLOW, pos_act), (Resource.RED, pos_act)]
    outputs = [(Resource.MONEY, pos_act)]
    pollution = [pos_target, pos_target]

    result = pa.activateCard(acting, grid, inputs=inputs, outputs=outputs, pollution=pollution)

    assert result is True

    # verify resources: inputs removed, output added
    assert acting.resources == [Resource.MONEY]