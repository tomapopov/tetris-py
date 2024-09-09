# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE
from typing import List
from unittest.mock import patch

from src.tetris.piece import Piece
from src.tetris.point import MinoPoint, Point, rotate_point_90, DIRECTION_SHIFT
from tests.conftest import pieces


def test_move(pieces: List[Piece]):

    for piece in pieces:
        for direction, (dx, dy) in DIRECTION_SHIFT.items():
            expected_points = {MinoPoint(p.x + dx, p.y + dy) for p in piece.points}
            expected_centre = Point(piece._centre.x + dx, piece._centre.y + dy)
            did_move = piece.move(direction)
            assert did_move
            assert set(piece.points) == expected_points
            assert expected_centre == piece._centre


def test_rotate(pieces: List[Piece]):
    for piece in pieces:
        expected_points = {rotate_point_90(p, piece._centre) for p in piece.points}
        expected_centre = piece._centre
        piece.rotate()
        assert set(piece.points) == expected_points
        assert expected_centre is piece._centre
