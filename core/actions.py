from enum import Enum

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    STAY = 4
    SHOOT = 5

    @classmethod
    def all(cls):
        return list(cls)
