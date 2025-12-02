import unittest
from typing import List
from game_observer import TerraFuturaObserverInterface, GameObserver

class MockObserver(TerraFuturaObserverInterface):
    def __init__(self, name: str = "MockObserver"):
        self.name = name
        self.received_states: List[str] = []

    def notify(self, game_state: str) -> None:
        self.received_states.append(game_state)

    def get_last_state(self) -> str:
        return self.received_states[-1] if self.received_states else ""

    def get_state_count(self) -> int:
        return len(self.received_states)

class TestGameObserver(unittest.TestCase):
    def setUp(self) -> None:
        self.observer = GameObserver()
        self.mock1 = MockObserver("Observer1")
        self.mock2 = MockObserver("Observer2")
        self.mock3 = MockObserver("Observer3")

    def test_add_observer(self) -> None:
        self.observer.add_observer(1, self.mock1)
        self.observer.add_observer(2, self.mock2)
        self.assertEqual(len(self.observer.observers), 2)
        self.assertIn(1, self.observer.observers)
        self.assertIn(2, self.observer.observers)
        self.assertEqual(self.observer.observers[1], self.mock1)
        self.assertEqual(self.observer.observers[2], self.mock2)

    def test_add_observer_overwrites(self) -> None:
        self.observer.add_observer(1, self.mock1)
        self.observer.add_observer(1, self.mock2)
        self.assertEqual(len(self.observer.observers), 1)
        self.assertEqual(self.observer.observers[1], self.mock2)

    def test_remove_observer(self) -> None:
        self.observer.add_observer(1, self.mock1)
        self.observer.add_observer(2, self.mock2)
        self.observer.remove_observer(1)
        self.assertEqual(len(self.observer.observers), 1)
        self.assertNotIn(1, self.observer.observers)
        self.assertIn(2, self.observer.observers)

    def test_remove_nonexistent_observer(self) -> None:
        self.observer.add_observer(1, self.mock1)
        self.observer.remove_observer(999)
        self.assertEqual(len(self.observer.observers), 1)
        self.assertIn(1, self.observer.observers)

    def test_notify_all_single_observer(self) -> None:
        self.observer.add_observer(1, self.mock1)
        new_state = {1: "Player 1 state"}
        self.observer.notify_all(new_state)
        self.assertEqual(self.mock1.get_state_count(), 1)
        self.assertEqual(self.mock1.get_last_state(), "Player 1 state")

    def test_notify_all_multiple_observers(self) -> None:
        self.observer.add_observer(1, self.mock1)
        self.observer.add_observer(2, self.mock2)
        self.observer.add_observer(3, self.mock3)
        new_state = {
            1: "State for player 1",
            2: "State for player 2",
            3: "State for player 3"
        }
        self.observer.notify_all(new_state)
        self.assertEqual(self.mock1.get_last_state(), "State for player 1")
        self.assertEqual(self.mock2.get_last_state(), "State for player 2")
        self.assertEqual(self.mock3.get_last_state(), "State for player 3")

    def test_notify_all_partial_observers(self) -> None:
        self.observer.add_observer(1, self.mock1)
        self.observer.add_observer(2, self.mock2)
        new_state = {1: "Only player 1 state"}
        self.observer.notify_all(new_state)
        self.assertEqual(self.mock1.get_state_count(), 1)
        self.assertEqual(self.mock2.get_state_count(), 0)

    def test_notify_all_empty_state(self) -> None:
        self.observer.add_observer(1, self.mock1)
        self.observer.notify_all({})
        self.assertEqual(self.mock1.get_state_count(), 0)

    def test_notify_all_no_observers(self) -> None:
        new_state = {1: "Some state"}
        self.observer.notify_all(new_state)
        self.assertEqual(len(self.observer.observers), 0)

    def test_observer_interface_abstract(self) -> None:
        observer = TerraFuturaObserverInterface()
        with self.assertRaises(NotImplementedError):
            observer.notify("test state")

if __name__ == "__main__":
    unittest.main()