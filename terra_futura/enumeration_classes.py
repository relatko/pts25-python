from enum import Enum

class Deck(Enum):
    I = "I"
    II = "II"

class Resource(Enum):
    GREEN = "Green"
    RED = "Red"
    YELLOW = "Yellow"
    BULB = "Bulb"
    GEAR = "Gear"
    CAR = "Car"
    MONEY = "Money"
    POLLUTION = "Pollution"

class CardSource(Enum):
    deck: Deck
    index: int

class GameState(Enum):
    TAKE_CARD_NO_CARD_DISCARDED = "TakeCardNoCardDiscarded"
    TAKE_CARD_CARD_DISCARDED = "TakeCardCardDiscarded"
    ACTIVATE_CARD = "ActivateCard"
    SELECT_REWARD = "SelectReward"
    SELECT_ACTIVATION_PATTERN = "SelectActivationPattern"
    SELECT_SCORING_METHOD = "SelectScoringMethod"
    FINISH = "Finish"