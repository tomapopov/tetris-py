from typing import List
from unittest.mock import MagicMock, patch

import pytest

from src.tetris.board import Board, _ROW_PADDING
from src.tetris.piece import Piece
from src.tetris.point import MinoPoint


@pytest.fixture
def board():
    return Board()


def test_reached_top_row(board: Board):
    # Set non-empty space in top row
    assert not board.reached_top_row()
    board._grid[_ROW_PADDING][0] = 1
    assert board.reached_top_row()


def test_reset(board: Board):
    initial_grid = board._grid
    board.reset()
    assert board._grid is not initial_grid
    assert sum(sum(row)for row in board._grid) == 0
    assert len(board._grid) == board.height + _ROW_PADDING
    assert len(board._grid[0]) == board.width


def test_add_piece(board: Board, pieces: List[Piece]):
    for piece in pieces:
        assert board.can_add_piece(piece)
        board.add_piece(piece)
        for p in piece.points:
            assert board.at_point(p) == piece.piece_index
        assert not board.can_add_piece(piece)
        board._remove_piece(piece)
        for p in piece.points:
            assert board.at_point(p) == 0
        assert board.can_add_piece(piece)
