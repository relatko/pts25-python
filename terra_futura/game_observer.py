from typing import Dict
from abc import ABC
from .interfaces import TerraFuturaObserverInterface

class GameObserver(TerraFuturaObserverInterface):
    """
    GameObserver manages a set of observers (one per player)
    and broadcasts game state changes to ALL of them.

    ######### Example Usage ##########

    class ConsoleObserver(TerraFuturaObserverInterface):
        def notify(self, game_state: str) -> None:
            print(f"[Observer] {game_state}")

    dispatcher = GameObserver()

    dispatcher.register_observer(1, ConsoleObserver())
    dispatcher.register_observer(2, ConsoleObserver())

    dispatcher.notify("Player 1 placed a card.")
    """

    def __init__(self):
        # Mapping: player_id -> observer instance
        self.observers: Dict[int, TerraFuturaObserverInterface] = {}

    def register_observer(self, player_id: int, observer: TerraFuturaObserverInterface) -> None:
        """Add a new observer for a given player."""
        self.observers[player_id] = observer

    def unregister_observer(self, player_id: int) -> None:
        """Remove an observer for a given player."""
        self.observers.pop(player_id, None)

    def notify(self, game_state: str) -> None:
        """
        Broadcast the game state to ALL registered observers.
        """
        for player_id, observer in self.observers.items():
            observer.notify(game_state)

