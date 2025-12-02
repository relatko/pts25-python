from typing import Dict

class TerraFuturaObserverInterface:
    def notify(self, game_state: str) -> None:
        raise NotImplementedError("Subclasses must implement notify()")

class GameObserver:
    def __init__(self):
        self.observers: Dict[int, 'TerraFuturaObserverInterface'] = {}

    def add_observer(self, player_id: int, observer: 'TerraFuturaObserverInterface') -> None:
        self.observers[player_id] = observer

    def remove_observer(self, player_id: int) -> None:
        if player_id in self.observers:
            del self.observers[player_id]

    def notify_all(self, new_state: Dict[int, str]) -> None:
        for player_id, state_string in new_state.items():
            if player_id in self.observers:
                self.observers[player_id].notify(state_string)