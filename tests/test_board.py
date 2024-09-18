from typing import List

import pytest

from src.tetris.board import Board, ROW_PADDING
from src.tetris.piece import Piece
from src.tetris.point import MinoPoint


@pytest.fixture
def board():
    return Board()


def test_reached_top_row(board: Board):
    # Set non-empty space in top row
    assert not board.reached_top_row()
    board._grid[ROW_PADDING][0] = 1
    assert board.reached_top_row()


def test_reset(board: Board):
    initial_grid = board._grid
    board.reset()
    assert board._grid is not initial_grid
    assert sum(sum(row)for row in board._grid) == 0
    assert len(board._grid) == board.height + ROW_PADDING
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


def test_clear_completed_rows(board: Board):
    for row in range(board._height - 2, board._height):
        for col in range(board.width):
            board._grid[row][col] = 1

    assert board._full_row(board._height - 1)
    assert board._full_row(board._height - 2)
    for row in range(board._height - 2):
        assert not board._full_row(row)

    num_removed = board.clear_completed_rows(list(range(board._height)))
    assert num_removed == 2
    for row in range(board._height):
        assert not board._full_row(row)


def test_space_below(board: Board):
    bottom_row_point = MinoPoint(0, board._height - 1)
    penultimate_row_point = MinoPoint(0, board._height - 2)
    assert not board.space_below(bottom_row_point)
    assert board.space_below(penultimate_row_point)
    board._grid[board._height - 1][0] = 1
    assert not board.space_below(penultimate_row_point)
