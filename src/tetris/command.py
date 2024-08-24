# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from enum import Enum
import pygame


class Command(Enum):
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    MOVE_BOTTOM = 4
    ROTATE = 5
    QUIT = 6
    HELP = 7
    PAUSE = 8
    RESTART = 9

    @classmethod
    def from_char(cls, char: str):
        if not char.isalpha():
            raise ValueError(f"Non-alphabet chars found in input: {char!r}")
        char = char.upper()
        mapping = {
            "L": cls.MOVE_LEFT,
            "R": cls.MOVE_RIGHT,
            "D": cls.MOVE_DOWN,
            "DD": cls.MOVE_BOTTOM,
            "U": cls.ROTATE,
            "Q": cls.QUIT,
            "H": cls.HELP,
            "P": cls.PAUSE,
        }
        if char not in mapping:
            raise ValueError(f"Unsupported input: {char!r}")
        return mapping[char]

    @classmethod
    def from_pygame_key(cls, key: int):
        mapping = {
            pygame.K_LEFT: cls.MOVE_LEFT,
            pygame.K_RIGHT: cls.MOVE_RIGHT,
            pygame.K_DOWN: cls.MOVE_DOWN,
            pygame.K_SPACE: cls.MOVE_BOTTOM,
            pygame.K_UP: cls.ROTATE,
            pygame.K_q: cls.QUIT,
            pygame.K_h: cls.HELP,
            pygame.K_p: cls.PAUSE,
            pygame.K_r: cls.RESTART,
        }
        if key not in mapping:
            raise ValueError(f"Unsupported pygame key: {key}")
        return mapping[key]