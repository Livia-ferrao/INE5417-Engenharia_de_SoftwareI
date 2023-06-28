from enum import Enum

class State(Enum):
    NOT_INITIALIZED = 1
    IN_PROGRESS = 2
    ABANDONED = 3
    FINISHED = 4
    WAITING_REMOTE_MOVE = 5

class Move(Enum):
    CONSTRUCTION = 1
    CHANGE = 2
    GIVE_UP = 3
    INITIAL = 4