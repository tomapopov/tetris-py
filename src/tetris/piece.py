# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from abc import ABC, abstractmethod
from typing import Tuple, List, Set, Type
import random

from .direction import Direction

from . import board

from .colours import (
    BLACK_COLOUR,
    CYAN_COLOUR,
    PINK_COLOUR,
    YELLOW_COLOUR,
    GREEN_COLOUR,
    RED_COLOUR,
    BLUE_COLOUR,
    PURPLE_COLOUR,
)
from .point import Point, MinoPoint


PIECE_COLOURS_ANSI = [
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
    def __init__(self, board: "board.Board", top_left: MinoPoint):
        ps, c = self.points_from_top_left(top_left)
        self._points: List[MinoPoint] = ps
        self._centre: Point = c
        self._board = board
        self._board.add_piece(self)

    @property
    def points(self) -> List[MinoPoint]:
        """
        :return: List of coordinates for the blocks which make up the piece
        """
        return self._points

    @classmethod
    @abstractmethod
    def points_from_top_left(cls, top_left: MinoPoint) -> Tuple[List[MinoPoint], Point]:
        """
        Calculates the blocks and rotational centre from the top left block coordinate
        :param top_left: the top left block coordinate
        :return: Tuple of: list of block coordinates for the piece, and the rotational centre
        """
        pass

    def rotate(self) -> None:
        """
        Rotates the piece on the board, if possible
        :return: None
        """
        new_points = [_rotate_90(p, self._centre) for p in self._points]
        if self._board.can_shift(self, new_points):
            # TODO: add "wall kick" functionality to rotate + shift the piece
            #  when its going to hit a wall or the stack from rotating
            old_points = self._points
            self._points = new_points
            # No need to update centre here
            self._board.update_piece_location(self, old_points)

    def shift(self, direction: Direction) -> bool:
        """
        Shifts the piece, if possible, in the given direction.
        :param direction: Direction
        :return: True if the piece moved successfully, False otherwise
        """
        new_points = [p.shift(direction) for p in self._points]
        if self._board.can_shift(self, new_points):
            old_points = self._points
            self._points = new_points
            self._centre = self._centre.shift(direction)
            self._board.update_piece_location(self, old_points)
            shifted = True
        else:
            shifted = False
        return shifted

    def can_shift_down(self) -> bool:
        """
        Checks if the piece can move down
        :return: True if it can shift downwards, False if not
        """
        for col in self._columns:
            lowest = self._lowest_block_in_col(col)
            if not self._board.space_below(lowest):
                return False
        return True

    @property
    def _columns(self) -> Set[int]:
        """
        The columns taken up by all the blocks that make up the piece
        :return: set of integer columns
        """
        return set(p.x for p in self._points)

    @property
    def rows(self) -> Set[int]:
        """
        The rows taken up by all the blocks that make up the piece
        :return: set of integer rows
        """
        return set(p.y for p in self._points)

    def _lowest_block_in_col(self, col: int) -> MinoPoint:
        """
        Finds the lowest block in a column, used to check ability to move down
        :param col: column value
        :return: coordinate of the lowest block in the given column for this piece
        """
        max_y = max(p.y for p in self._points if p.x == col)
        matches = [p for p in self._points if p.x == col and p.y == max_y]
        assert len(matches) == 1, f"How did we not find the lowest piece in col {col!r}?!"
        return matches[0]

    @classmethod
    @property
    @abstractmethod
    def piece_index(self) -> int:
        ...

    @classmethod
    @property
    @abstractmethod
    def letter(self) -> str:
        ...


class IPiece(Piece):
    piece_index: int = 1
    letter: str = "I"

    @classmethod
    def points_from_top_left(self, top_left: MinoPoint):
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x + 1, top_left.y),
            MinoPoint(top_left.x + 2, top_left.y),
            MinoPoint(top_left.x + 3, top_left.y),
        ]
        return points, Point(points[1].x + 0.5, top_left.y + 0.5)


class JPiece(Piece):
    piece_index: int = 2
    letter: str = "J"

    @classmethod
    def points_from_top_left(cls, top_left: MinoPoint):
        next_row_idx = top_left.y + 1
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x, next_row_idx),
            MinoPoint(top_left.x + 1, next_row_idx),
            MinoPoint(top_left.x + 2, next_row_idx),
        ]
        return points, points[2]


class LPiece(Piece):
    piece_index: int = 3
    letter: str = "L"

    @classmethod
    def points_from_top_left(cls, top_left: MinoPoint):
        next_row_idx = top_left.y + 1
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x - 2, next_row_idx),
            MinoPoint(top_left.x - 1, next_row_idx),
            MinoPoint(top_left.x, next_row_idx),
        ]
        return points, points[2]


class OPiece(Piece):
    piece_index: int = 4
    letter: str = "O"

    @classmethod
    def points_from_top_left(cls, top_left: MinoPoint):
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x + 1, top_left.y),
            MinoPoint(top_left.x, top_left.y + 1),
            MinoPoint(top_left.x + 1, top_left.y + 1),
        ]
        return points, Point(top_left.x + 0.5, top_left.y + 0.5)



class SPiece(Piece):
    piece_index: int = 5
    letter: str = "S"

    @classmethod
    def points_from_top_left(cls, top_left: MinoPoint):
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x + 1, top_left.y),
            MinoPoint(top_left.x - 1, top_left.y + 1),
            MinoPoint(top_left.x, top_left.y + 1),
        ]
        return points, points[3]


class TPiece(Piece):
    piece_index: int = 6
    letter: str = "T"


    @classmethod
    def points_from_top_left(cls, top_left: MinoPoint):
        next_row_idx = top_left.y + 1
        points = [
            MinoPoint(top_left.x, top_left.y),
            MinoPoint(top_left.x - 1, next_row_idx),
            MinoPoint(top_left.x, next_row_idx),
            MinoPoint(top_left.x + 1, next_row_idx),
        ]
        return points, points[2]


class ZPiece(Piece):
    piece_index: int = 7
    letter: str = "Z"

    @classmethod
    def points_from_top_left(cls, top_left: MinoPoint):
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


SHAPE_POSSIBILITIES = [IPiece, ZPiece, LPiece, JPiece, SPiece, TPiece, OPiece]


def new_piece_type() -> Type[Piece]:
    return random.choice(SHAPE_POSSIBILITIES)

class PieceGenerator:
    """
    Simple class used to generate and show what the next piece shape will be
    """

    def __init__(self):
        self._next_piece_type = new_piece_type()

    @property
    def next_piece_type(self) -> Type[Piece]:
        """
        The next piece type after the current
        :return: The type of piece
        """
        return self._next_piece_type

    def generate_new_piece_type(self) -> Type[Piece]:
        """
        Generates a new next piece shape
        :return: The type of piece
        """
        ret = self._next_piece_type
        self._next_piece_type = new_piece_type()
        return ret
