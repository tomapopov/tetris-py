import random
from threading import Lock
from typing import List

from piece import Piece, new_piece_type, PIECE_COLOURS
from point import MinoPoint

MARKER = "X"
Grid = List[List[int]]

class Board:

    def __init__(self, height: int = 20, width: int = 10):
        # grid with 2 extra rows for generating new pieces at random at the top
        self._padding = 0
        self._height = height
        self._width = width
        self._grid: Grid = self._new_rows(height + self._padding, width)
        self._lock = Lock()

    def new_piece(self) -> Piece:
        # TODO: know when the game is over - when we can introduce new pieces!
        # TODO: introduce smarter logic for starting location of piece ?
        # the +2 and -3 used here is to make sure all pieces can fit e.g 'I' piece has another 3 mino blocks on the right of the
        # top left
        top_left = MinoPoint(random.randint(0 + 2, self._width - 1 - 3), 0)
        piece_type = new_piece_type()
        piece = piece_type(self, top_left)
        return piece

    def clear_completed_rows(self) -> int:
        removed = 0
        with self.lock:
            for i in range(self._height - 1, 0 + self._padding, -1):
                if self._full_row(i):
                    self._remove_row(i)
                    removed += 1
            self._grid = self._new_rows(removed, self._width) + self._grid
        return removed

    def _full_row(self, idx: int) -> bool:
        row = self._grid[idx]
        return all(x > 0 for x in row)

    def _remove_row(self, idx: int) -> None:
        self._grid.pop(idx)

    @staticmethod
    def _new_rows(height: int, width: int) -> Grid:
        return [[0] * width for _ in range(height)]

    def update_piece_location(self, piece: Piece, old_points: List[MinoPoint]) -> None:
        for p in old_points:
            self._set_at_point(p, 0)
        self.add_piece(piece)

    def _remove_piece(self, piece: Piece) -> None:
        for p in piece.points:
            assert self._at_point(p) == piece.colour_code
        for p in piece.points:
            self._set_at_point(p, 0)

    def _at_point(self, p: MinoPoint) -> int:
        return self._grid[p.y][p.x]

    def _set_at_point(self, p: MinoPoint, val: int) -> None:
        self._grid[p.y][p.x] = val

    def can_shift(self, piece: Piece, new_points: List[MinoPoint]) -> bool:
        self._remove_piece(piece)
        res = True
        for p in new_points:
            if self._point_outside_grid(p) or self._at_point(p) > 0:
                res = False
                break
        self.add_piece(piece)
        return res

    def add_piece(self, piece: Piece) -> None:
        for p in piece.points:
            assert self._at_point(p) == 0
        for p in piece.points:
            self._set_at_point(p, piece.colour_code)

    def space_below(self, point: MinoPoint) -> bool:
        below_y = point.y + 1
        if self._point_outside_grid(MinoPoint(point.x, below_y)):
            return False
        return self._grid[below_y][point.x] == 0

    def _point_outside_grid(self, point: MinoPoint) -> bool:
        return (not (0 - self._padding <= point.y < self._height)) or (not (0 <= point.x < self._width))

    def __str__(self) -> str:
        res = []
        for row in self._grid[self._padding:]:
            row_res = []
            for x in row:
                assert isinstance(x, int)
                marker = "X" if x > 0 else "0"
                row_res.append(PIECE_COLOURS[x].format(marker))
            res.append(" ".join(row_res))
        pretty_grid = "\n".join(res)
        return str(pretty_grid)

    @property
    def lock(self) -> Lock:
        return self._lock

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width