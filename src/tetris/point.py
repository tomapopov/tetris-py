# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from dataclasses import dataclass

from .direction import Direction


DIRECTION_SHIFT = {
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
    Direction.UP: (0, -1),
}


@dataclass(frozen=True)
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
        x_shift, y_shift = DIRECTION_SHIFT[direction]
        return cls(self.x + x_shift, self.y + y_shift)


@dataclass(frozen=True)
class MinoPoint(Point):
    x: int
    y: int


def rotate_point_90(p: MinoPoint, centre: Point, reverse: bool = False) -> MinoPoint:
    """
    Rotates a point about the centre through 90 degrees
    :param p: the coordinate point
    :return: a new point constructed by rotating the given point
    """

    # Shift point to origin
    x = p.x - centre.x
    y = p.y - centre.y

    cos_angle = 0
    sin_angle = -1 if reverse else 1
    # Apply transformation
    new_x = x * cos_angle - y * sin_angle
    new_y = x * sin_angle + y * cos_angle

    # Shift back to original coordinates
    new_x += centre.x
    new_y += centre.y

    if new_x == p.x and new_y == p.y:
        # Don't create a whole new object for the same point
        return p
    return MinoPoint(int(new_x), int(new_y))
