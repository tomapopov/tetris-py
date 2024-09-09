from unittest.mock import MagicMock

import pytest

from src.tetris.board import Board
from src.tetris.piece import IPiece, JPiece, LPiece, OPiece, SPiece, TPiece, ZPiece
from src.tetris.point import MinoPoint


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
