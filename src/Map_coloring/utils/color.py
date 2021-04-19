from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4

    @classmethod
    def get_list(cls):
        return [e for e in Color]
