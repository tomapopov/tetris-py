from enum import Enum


class Direction(Enum):
    DOWN = 1
    RIGHT = 2
    LEFT = 3

    @classmethod
    def from_char(cls, char: str):
        mapping = {
            "L": Direction.LEFT,
            "R": Direction.RIGHT,
            "D": Direction.DOWN,
        }
        if char not in mapping:
            raise ValueError(f"Unsupported direction character {char!r}")
        return mapping[char]