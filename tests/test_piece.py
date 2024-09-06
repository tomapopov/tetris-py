# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE
from typing import List
from unittest.mock import MagicMock, patch
import pytest

from src.tetris.board import Board
from src.tetris.direction import Direction
from src.tetris.piece import IPiece, TPiece, ZPiece, SPiece, OPiece, LPiece, JPiece, Piece
from src.tetris.point import MinoPoint, Point, rotate_point_90


@pytest.fixture
def i_piece():
    return IPiece(MagicMock(spec=Board), MinoPoint(5, 5))


@pytest.fixture
def j_piece():
    return JPiece(MagicMock(spec=Board), MinoPoint(5, 5))


@pytest.fixture
def l_piece():
    return LPiece(MagicMock(spec=Board), MinoPoint(5, 5))


@pytest.fixture
def o_piece():
    return OPiece(MagicMock(spec=Board), MinoPoint(5, 5))


@pytest.fixture
def s_piece():
    return SPiece(MagicMock(spec=Board), MinoPoint(5, 5))


@pytest.fixture
def t_piece():
    return TPiece(MagicMock(spec=Board), MinoPoint(5, 5))


@pytest.fixture
def z_piece():
    return ZPiece(MagicMock(spec=Board), MinoPoint(5, 5))


@pytest.fixture
def pieces(j_piece, l_piece, o_piece, s_piece, t_piece, z_piece):
     return [j_piece, l_piece, o_piece, s_piece, t_piece, z_piece]


def test_move(pieces: List[Piece]):
    directions_and_change = [
        (Direction.DOWN, (0, 1)),
        (Direction.LEFT, (-1, 0)),
        (Direction.RIGHT, (1, 0)),
    ]
    for piece in pieces:
        with patch.object(piece._board, "can_shift", return_value=True):
            for direction, (dx, dy) in directions_and_change:
                expected_points = {MinoPoint(p.x + dx, p.y + dy) for p in piece.points}
                expected_centre = Point(piece._centre.x + dx, piece._centre.y + dy)
                did_move = piece.move(direction)
                assert did_move
                assert set(piece.points) == expected_points
                assert expected_centre == piece._centre


def test_rotate(pieces: List[Piece]):
    for piece in pieces:
        with patch.object(piece._board, "can_shift", return_value=True):
            expected_points = {rotate_point_90(p, piece._centre) for p in piece.points}
            expected_centre = piece._centre
            piece.rotate()
            assert set(piece.points) == expected_points
            assert expected_centre is piece._centre
