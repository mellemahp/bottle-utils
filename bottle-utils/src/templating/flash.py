
from enum import Enum

class FlashLvl(Enum):
    INFO = 0
    WARN = 1
    ERROR = 2


class Flash(): 
    def __init__(self, level, message): 
        if not isinstance(level, FlashLvl):
            raise ValueError("level must be a valid FlashLvl")

        self._level = level
        self.msg = message

    @property
    def lvl(self): 
        return self._level.name.lower()