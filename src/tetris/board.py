# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

import random
from typing import List, Type

from . import piece
from .point import MinoPoint

Grid = List[List[int]]
_ROW_PADDING = 2


class Board:

    def __init__(self, height: int = 20, width: int = 10):
        # grid with 2 extra rows for generating new pieces at random at the top
        self._height = height + _ROW_PADDING
        self._width = width
        self.reset()

    def reset(self) -> None:
        self._grid: Grid = self._new_rows(self._height, self._width)

    def reached_top_row(self) -> bool:
        """
        Checks if stack has reached the top row
        :return: True if there are blocks in top row, False otherwise
        """
        top_playable_row = self._grid[_ROW_PADDING]
        return sum(top_playable_row) > 0

    def clear_completed_rows(self, rows: List[int]) -> int:
        """
        Checks if any rows are complete and removes them
        :param rows: the rows to check
        :return: the number of rows cleared
        """
        rows = sorted(rows, reverse=True)
        removed = 0
        for i in rows:
            if self._full_row(i):
                self._remove_row(i)
                removed += 1
        self._grid = self._new_rows(removed, self._width) + self._grid
        return removed

    def can_add_piece(self, piece: "piece.Piece"):
        """
        Checks if a piece can be added to the board
        :param piece: the piece
        :return: True if possible to add, False otherwise
        """
        for p in piece.points:
            if self._point_outside_grid(p) or self._at_point(p) > 0:
                return False
        return True

    def add_piece(self, piece: "piece.Piece") -> None:
        """
        Adds a piece to the board
        :param piece: the piece to add
        :return: None
        """
        for p in piece.points:
            assert self._at_point(p) == 0
        for p in piece.points:
            self._set_at_point(p, piece.piece_index)

    def space_below(self, point: MinoPoint) -> bool:
        """
        Checks if there is empty space below a block
        :param point: the coordinate
        :return: True if empty space underneath, False otherwise
        """
        below_point = MinoPoint(point.x, point.y + 1)
        if self._point_outside_grid(below_point):
            return False
        return self._at_point(below_point) == 0

    @property
    def height(self) -> int:
        """
        Public height value used by other components
        :return: integer height
        """
        # subtract the row padding for the public height value used by other components, as this is a detail
        # internal to the board logic. Other components don't need to be aware of it.
        return self._height - _ROW_PADDING

    @property
    def width(self) -> int:
        """
        Public width value used by other components
        :return: integer width
        """
        return self._width

    def value_at(self, i: int, j: int) -> int:
        """
        Gets the value at the coordinate
        :param i: row
        :param j: column
        :return: integer code of the piece at that coordinate
        """
        return self._grid[i + _ROW_PADDING][j]

    def _full_row(self, idx: int) -> bool:
        row = self._grid[idx]
        return all(x > 0 for x in row)

    def _remove_row(self, idx: int) -> None:
        self._grid.pop(idx)

    @staticmethod
    def _new_rows(height: int, width: int) -> Grid:
        return [[0] * width for _ in range(height)]

    def _remove_piece(self, piece: "piece.Piece") -> None:
        for p in piece.points:
            assert self._at_point(p) == piece.piece_index
        for p in piece.points:
            self._set_at_point(p, 0)

    def _at_point(self, p: MinoPoint) -> int:
        return self._grid[p.y][p.x]

    def _set_at_point(self, p: MinoPoint, val: int) -> None:
        self._grid[p.y][p.x] = val

    def _point_outside_grid(self, point: MinoPoint) -> bool:
        return (not (0 <= point.y < self._height)) or (not (0 <= point.x < self._width))

    def __str__(self) -> str:
        res = []
        for row in self._grid[_ROW_PADDING:]:
            row_res = []
            for x in row:
                assert isinstance(x, int)
                marker = "X" if x > 0 else "0"
                row_res.append(piece.PIECE_COLOURS_ANSI[x].format(marker))
            res.append(" ".join(row_res))
        pretty_grid = "\n".join(res)
        return str(pretty_grid)