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