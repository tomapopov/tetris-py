import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, List, Set, Type

from direction import Direction
import random

from colours import (
    BLACK_COLOUR,
    CYAN_COLOUR,
    PINK_COLOUR,
    YELLOW_COLOUR,
    GREEN_COLOUR,
    RED_COLOUR,
    BLUE_COLOUR,
    PURPLE_COLOUR,
)

PI_DIV_2 = math.pi / 2

@dataclass
class Point:
    x: float
    y: float


@dataclass
class MinoPoint(Point):
    x: int
    y: int


PIECE_COLOURS = [
    "\033[37m{}\033[00m",  # white, for empty spaces
    "\033[96m{}\033[00m",
    "\033[95m{}\033[00m",
    "\033[93m{}\033[00m",
    "\033[92m{}\033[00m",
    "\033[91m{}\033[00m",
    "\033[34m{}\033[00m",
    "\033[35m{}\033[00m",
]
PIECE_COLOURS_RGB = [
    BLACK_COLOUR,
    CYAN_COLOUR,
    PINK_COLOUR,
    YELLOW_COLOUR,
    GREEN_COLOUR,
    RED_COLOUR,
    BLUE_COLOUR,
    PURPLE_COLOUR
]

class Piece(ABC):
    def __init__(self, board: "Board", top_left: MinoPoint):
        ps, c = self._init_state(top_left)
        self._points: List[MinoPoint] = ps
        self._centre: Point = c
        self._board = board
        self._board.add_piece(self)

    @property
    def points(self) -> List[MinoPoint]:
        return self._points

    @abstractmethod
    def _init_state(self, top_left: MinoPoint) -> Tuple[List[MinoPoint], Point]:
        pass

    def rotate(self):
        # TODO: check if rotated piece can fit on current board!
        with self._board.lock:
            old_points = self._points
            self._points = [_rotate_90(p, self._centre) for p in self._points]
            self._board.update_piece_location(self, old_points)

    def shift(self, direction: Direction) -> bool:
        with self._board.lock:
            match direction:
                case Direction.DOWN: return self._shift_down()
                case Direction.RIGHT: return self._shift_right()
                case Direction.LEFT: return self._shift_left()
                case _: raise ValueError(f"Unsupported direction: {direction!r}")

    def _shift_down(self) -> bool:
        if not self.can_shift_down():
            return False

        old_points = self._points
        new_points = [MinoPoint(p.x, p.y + 1) for p in self._points]
        self._points = new_points
        self._centre = Point(self._centre.x, self._centre.y + 1)
        self._board.update_piece_location(self, old_points)
        return True

    def _shift_left(self) -> bool:
        if not self._can_shift_left():
            return False

        old_points = self._points
        new_points = [MinoPoint(p.x - 1, p.y) for p in self._points]
        self._points = new_points
        self._centre = Point(self._centre.x - 1, self._centre.y)
        self._board.update_piece_location(self, old_points)
        return True

    def _shift_right(self) -> bool:
        if not self._can_shift_right():
            return False

        old_points = self._points
        new_points = [MinoPoint(p.x + 1, p.y) for p in self._points]
        self._points = new_points
        self._centre = Point(self._centre.x + 1, self._centre.y)
        self._board.update_piece_location(self, old_points)
        return True


    def can_shift_down(self) -> bool:
        for col in self._columns:
            lowest = self._lowest_block_in_col(col)
            if not self._board.space_below(lowest):
                return False
        return True

    def _can_shift_right(self) -> bool:
        for row in self._rows:
            right_most = self._right_most_block_in_row(row)
            if not self._board.space_on_right(right_most):
                return False
        return True

    def _can_shift_left(self) -> bool:
        for row in self._rows:
            left_most = self._left_most_block_in_row(row)
            if not self._board.space_on_left(left_most):
                return False
        return True

    @property
    def _columns(self) -> Set[int]:
        return set(p.x for p in self._points)

    @property
    def _rows(self) -> Set[int]:
        return set(p.y for p in self._points)

    def _lowest_block_in_col(self, col: int) -> MinoPoint:
        max_y = max(p.y for p in self._points if p.x == col)
        matches = [p for p in self._points if p.x == col and p.y == max_y]
        assert len(matches) == 1, f"How did we not find the lowest piece in col {col!r}?!"
        return matches[0]

    def _right_most_block_in_row(self, row: int) -> MinoPoint:
        max_x = max(p.x for p in self._points if p.y == row)
        matches = [p for p in self._points if p.y == row and p.x == max_x]
        assert len(matches) == 1, f"How did we not find the right-most piece in row {row!r}?!"
        return matches[0]

    def _left_most_block_in_row(self, row: int) -> MinoPoint:
        min_x = min(p.x for p in self._points if p.y == row)
        matches = [p for p in self._points if p.y == row and p.x == min_x]
        assert len(matches) == 1, f"How did we not find the left-most piece in row {row!r}?!"
        return matches[0]

    @property
    @abstractmethod
    def colour_code(self) -> int:
        ...

class IPiece(Piece):

    @property
    def colour_code(self) -> int:
        return 1

    def _init_state(self, top_left: MinoPoint):
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x + 1, top_left.y),
            MinoPoint(top_left.x + 2, top_left.y),
            MinoPoint(top_left.x + 3, top_left.y),
        ]
        return points, Point(points[1].x + 0.5, top_left.y + 0.5)


class JPiece(Piece):

    @property
    def colour_code(self) -> int:
        return 2

    def _init_state(self, top_left: MinoPoint):
        next_row_idx = top_left.y + 1
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x, next_row_idx),
            MinoPoint(top_left.x + 1, next_row_idx),
            MinoPoint(top_left.x + 2, next_row_idx),
        ]
        return points, points[2]


class LPiece(Piece):

    @property
    def colour_code(self) -> int:
        return 3

    def _init_state(self, top_left: MinoPoint):
        next_row_idx = top_left.y + 1
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x - 2, next_row_idx),
            MinoPoint(top_left.x - 1, next_row_idx),
            MinoPoint(top_left.x, next_row_idx),
        ]
        return points, points[2]


class OPiece(Piece):

    @property
    def colour_code(self) -> int:
        return 4

    def _init_state(self, top_left: MinoPoint):
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x + 1, top_left.y),
            MinoPoint(top_left.x, top_left.y + 1),
            MinoPoint(top_left.x + 1, top_left.y + 1),
        ]
        return points, Point(top_left.x + 0.5, top_left.y + 0.5)



class SPiece(Piece):

    @property
    def colour_code(self) -> int:
        return 5

    def _init_state(self, top_left: MinoPoint):
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x + 1, top_left.y),
            MinoPoint(top_left.x - 1, top_left.y + 1),
            MinoPoint(top_left.x, top_left.y + 1),
        ]
        return points, points[3]


class TPiece(Piece):

    @property
    def colour_code(self) -> int:
        return 6

    def _init_state(self, top_left: MinoPoint):
        next_row_idx = top_left.y + 1
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x - 1, next_row_idx),
            MinoPoint(top_left.x , next_row_idx),
            MinoPoint(top_left.x + 1, next_row_idx),
        ]
        return points, points[2]


class ZPiece(Piece):

    @property
    def colour_code(self) -> int:
        return 7

    def _init_state(self, top_left: MinoPoint):
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x + 1, top_left.y),
            MinoPoint(top_left.x + 1, top_left.y + 1),
            MinoPoint(top_left.x + 2, top_left.y + 1),
        ]
        return points, points[2]


def _rotate_90(p: MinoPoint, centre: Point) -> MinoPoint:
    """
    Rotates a point about the origin (0,0) through 90 degrees
    :param p: the coordinate point
    :return: a new point constructed by rotating the given point
    """

    # Shift point to origin
    x = p.x - centre.x
    y = p.y - centre.y

    cos_angle = 0
    sin_angle = 1
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


_SHAPE_POSSIBILITIES = [IPiece, ZPiece, LPiece, JPiece, SPiece, TPiece, OPiece]


def new_piece_type() -> Type[Piece]:
    return random.choice(_SHAPE_POSSIBILITIES)
