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
from .point import Point, MinoPoint, rotate_point_90

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
        self._board._remove_piece(self)
        self._rotate()
        if self._board.can_add_piece(self):
            self._board.add_piece(self)
            return
        # If the rotation isn't possible, undo it
        self._rotate(reverse=True)
        self._board.add_piece(self)

    def move(self, direction: Direction) -> bool:
        """
        Moves the piece in the given direction, if possible
        :param direction: Direction
        :return: True if the piece moved successfully, False otherwise
        """
        self._board._remove_piece(self)
        self._move(direction)
        if self._board.can_add_piece(self):
            self._board.add_piece(self)
            return True
        # If the move isn't possible, undo it
        self._move(direction.opposite)
        self._board.add_piece(self)
        return False

    def _move(self, direction: Direction) -> None:
        self._points = [p.shift(direction) for p in self._points]
        self._centre = self._centre.shift(direction)

    def _rotate(self, reverse: bool = False):
        self._points = [rotate_point_90(p, self._centre, reverse=reverse) for p in self._points]

    def can_shift_down(self) -> bool:
        """
        Checks if the piece can move down
        :return: True if it can shift downwards, False if not
        """
        return all(self._board.space_below(self._lowest_block_in_col(col)) for col in self.columns)

    def lowest_possible_position(self) -> List[MinoPoint]:
        """
        Calculates the lowest place that this piece could be on the boards
        :return: A list of the points marking the tetrimino's lowest possible position
        """
        min_dist = float("inf")
        for col in self.columns:
            row  = self._lowest_block_in_col(col).y
            dist = self._board.distance_to_stack(row, col)
            if dist < min_dist:
                min_dist = dist
        return [MinoPoint(p.x, p.y + min_dist) for p in self._points]

    @property
    def columns(self) -> Set[int]:
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
        centre = points[2]
        return points, Point(centre.x, centre.y)


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
        centre = points[2]
        return points, Point(centre.x, centre.y)


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
        centre = points[3]
        return points, Point(centre.x, centre.y)


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
        centre = points[2]
        return points, Point(centre.x, centre.y)


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
        centre = points[2]
        return points, Point(centre.x, centre.y)


SHAPE_POSSIBILITIES = [IPiece, ZPiece, LPiece, JPiece, SPiece, TPiece, OPiece]


def new_piece_type() -> Type[Piece]:
    return random.choice(SHAPE_POSSIBILITIES)


class PieceGenerator:
    """
    Simple class used to generate and show what the next piece shape will be
    """

    def __init__(self, board: "board.Board"):
        self._next_piece_type = new_piece_type()
        self._board = board

    @property
    def next_piece_type(self) -> Type[Piece]:
        """
        The next piece type after the current
        :return: The type of piece
        """
        return self._next_piece_type

    def _generate_new_piece_type(self) -> Type[Piece]:
        """
        Generates a new piece shape
        :return: The type of piece
        """
        piece_cls = self._next_piece_type
        self._next_piece_type = new_piece_type()
        return piece_cls

    def generate_new_piece(self) -> Piece:
        """
        Generates a new piece
        :return: The new piece
        """
        piece_cls = self._generate_new_piece_type()

        # TODO: use smarter logic for starting location of piece ?
        # the +2 on the x and -3 on the y coordinates are used here to make sure all pieces can fit
        # e.g 'I' piece has another 3 mino blocks on the right of the top left mino,
        # and L has 2 on the left
        top_left = MinoPoint(random.randint(0 + 2, self._board.width - 1 - 3), 0)
        piece = piece_cls(self._board, top_left)
        return piece

    def reset(self):
        self._generate_new_piece_type()
