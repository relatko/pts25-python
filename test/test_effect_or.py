# test_effect_or.py
from typing import List
from dataclasses import dataclass

import pytest

from terra_futura.interfaces import Resource, Effect
from terra_futura.effect_or import EffectOr
from terra_futura.arbitrary_basic import ArbitraryBasic
from terra_futura.transformation_fixed import TransformationFixed


@dataclass
class AlwaysTrueEffect(Effect):
    assistance: bool = False
    label: str = "true"

    def check(self, input: List[Resource], output: List[Resource], pollution: int) -> bool:
        return True

    def hasAssistance(self) -> bool:
        return self.assistance

    def state(self) -> str:
        return f"{self.label}"


@dataclass
class AlwaysFalseEffect(Effect):
    assistance: bool = False
    label: str = "false"

    def check(self, input: List[Resource], output: List[Resource], pollution: int) -> bool:
        return False

    def hasAssistance(self) -> bool:
        return self.assistance

    def state(self) -> str:
        return f"{self.label}"


# --- Tests for EffectOr basic logic -------------------------------------------


def test_effect_or_empty_returns_false():
    """If EffectOr has no children, check() should always return False."""
    eff_or = EffectOr(effects=[])
    assert eff_or.check([], [], 0) is False


def test_effect_or_all_false_returns_false():
    """If all children return False, EffectOr.check() must be False."""
    e1 = AlwaysFalseEffect()
    e2 = AlwaysFalseEffect()
    eff_or = EffectOr(effects=[e1, e2])

    assert eff_or.check([], [], 0) is False


def test_effect_or_any_true_returns_true():
    """If at least one child returns True, EffectOr.check() must be True."""
    e1 = AlwaysFalseEffect()
    e2 = AlwaysTrueEffect()
    e3 = AlwaysFalseEffect()
    eff_or = EffectOr(effects=[e1, e2, e3])

    assert eff_or.check([], [], 0) is True


def test_effect_or_has_assistance_if_any_child_has_assistance():
    """hasAssistance() should be True if ANY child has assistance."""
    e1 = AlwaysFalseEffect(assistance=False)
    e2 = AlwaysTrueEffect(assistance=True)
    e3 = AlwaysTrueEffect(assistance=False)

    eff_or = EffectOr(effects=[e1, e2, e3])
    assert eff_or.hasAssistance() is True


def test_effect_or_has_no_assistance_if_no_child_has_assistance():
    """hasAssistance() should be False if NO child has assistance."""
    e1 = AlwaysFalseEffect(assistance=False)
    e2 = AlwaysTrueEffect(assistance=False)

    eff_or = EffectOr(effects=[e1, e2])
    assert eff_or.hasAssistance() is False


def test_effect_or_state_empty():
    """state() for empty EffectOr should be '(empty OR)'."""
    eff_or = EffectOr(effects=[])
    assert eff_or.state() == "(empty OR)"


def test_effect_or_state_combines_child_states():
    """state() should join child states using ' OR ' and wrap in parentheses."""
    e1 = AlwaysTrueEffect(label="A")
    e2 = AlwaysFalseEffect(label="B")
    e3 = AlwaysTrueEffect(label="C")

    eff_or = EffectOr(effects=[e1, e2, e3])

    assert eff_or.state() == "(A OR B OR C)"


# --- Tests using real input / output / pollution with real Effect classes -----


@dataclass(frozen=True)
class DummyResource:
    """Simple, hashable resource stand-in for tests."""
    name: str


def _make_dummy_resources(*names: str) -> List[DummyResource]:
    return [DummyResource(name) for name in names]


# --- Tests using real input / output / pollution with real Effect classes -----


def test_effect_or_matches_transformation_fixed_with_correct_io_and_pollution():
    """
    EffectOr should return True when the given (input, output, pollution)
    matches its TransformationFixed child.
    """
    # Create specific dummy resource instances
    wood, brick = _make_dummy_resources("wood", "brick")

    trans = TransformationFixed(
        from_=[wood],     # must pay exactly [wood]
        to=[brick],       # get exactly [brick]
        pollution=1       # produce 1 pollution
    )

    eff_or = EffectOr(effects=[trans])

    # Correct triple → should match
    assert eff_or.check(input=[wood], output=[brick], pollution=1) is True

    # Wrong input → should fail
    assert eff_or.check(input=[brick], output=[brick], pollution=1) is False

    # Wrong output → should fail
    assert eff_or.check(input=[wood], output=[wood], pollution=1) is False

    # Wrong pollution → should fail
    assert eff_or.check(input=[wood], output=[brick], pollution=0) is False


def test_effect_or_matches_arbitrarybasic_with_correct_count_and_pollution():
    """
    EffectOr should return True when (input, output, pollution) matches
    its ArbitraryBasic child: correct length of input, correct output, correct pollution.
    """
    # Create resources
    r1, r2, reward = _make_dummy_resources("r1", "r2", "reward")

    arb = ArbitraryBasic(
        from_=2,              # pay ANY 2 resources
        to=[reward],          # gain [reward]
        pollution=1
    )

    eff_or = EffectOr(effects=[arb])

    # Correct: length(input) == 2, output == [reward], pollution == 1
    assert eff_or.check(input=[r1, r2], output=[reward], pollution=1) is True

    # Wrong: not enough input
    assert eff_or.check(input=[r1], output=[reward], pollution=1) is False

    # Wrong: too much input
    assert eff_or.check(input=[r1, r2, reward], output=[reward], pollution=1) is False

    # Wrong: output does not match
    assert eff_or.check(input=[r1, r2], output=[r1], pollution=1) is False

    # Wrong: pollution does not match
    assert eff_or.check(input=[r1, r2], output=[reward], pollution=0) is False


def test_effect_or_picks_any_matching_child_with_io_and_pollution():
    """
    With multiple children, EffectOr should accept if *any* Effect matches
    the given (input, output, pollution), and reject otherwise.
    """
    # Resources for TransformationFixed
    wood, brick = _make_dummy_resources("wood", "brick")
    trans = TransformationFixed(
        from_=[wood],
        to=[brick],
        pollution=0
    )

    # Resources for ArbitraryBasic
    r1, r2, money = _make_dummy_resources("r1", "r2", "money")
    arb = ArbitraryBasic(
        from_=2,
        to=[money],
        pollution=1
    )

    eff_or = EffectOr(effects=[trans, arb])

    # Matches TransformationFixed (first child)
    assert eff_or.check(input=[wood], output=[brick], pollution=0) is True

    # Matches ArbitraryBasic (second child)
    assert eff_or.check(input=[r1, r2], output=[money], pollution=1) is True

    # Matches neither
    assert eff_or.check(input=[wood, brick], output=[money], pollution=0) is False