from enum import Enum

from command import Command


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



    @classmethod
    def from_command(cls, command: Command):
        mapping = {
            Command.MOVE_LEFT: cls.LEFT,
            Command.MOVE_RIGHT: cls.RIGHT,
            Command.MOVE_DOWN: cls.DOWN,
            Command.MOVE_BOTTOM: cls.DOWN,
        }
        if command not in mapping:
            raise ValueError(f"Command {command} cannot be mapped to a direction")
        return mapping[command]