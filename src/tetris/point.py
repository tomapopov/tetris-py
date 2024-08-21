# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from dataclasses import dataclass

from .direction import Direction

_DIRECTION_SHIFT = {
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
}
@dataclass
class Point:
    x: float
    y: float

    def shift(self, direction: Direction) -> "Point":
        """
        Creates a new point object with coordinates equivalent to shifting this piece
        :param direction: the direction of movement
        :return: the new point
        """
        cls = type(self)
        x_shift, y_shift = _DIRECTION_SHIFT[direction]
        return cls(self.x + x_shift, self.y + y_shift)


@dataclass
class MinoPoint(Point):
    x: int
    y: int
