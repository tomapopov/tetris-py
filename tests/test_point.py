import pytest

from src.tetris.direction import Direction
from src.tetris.point import MinoPoint, Point, rotate_point_90


@pytest.mark.parametrize("point, direction, expected", [
    (MinoPoint(1, 0), Direction.DOWN, MinoPoint(1, 1)),
    (MinoPoint(-1, 2), Direction.LEFT, MinoPoint(-2, 2)),
    (MinoPoint(3, 2), Direction.RIGHT, MinoPoint(4, 2)),

    (Point(1.5, 0.0), Direction.DOWN, Point(1.5, 1.0)),
    (Point(-1.5, 2.3), Direction.LEFT, Point(-2.5, 2.3)),
    (Point(3.2, 2.0), Direction.RIGHT, Point(4.2, 2.0)),

])
def test_shift(point: Point, direction: Direction, expected: Point):
    result = point.shift(direction)
    assert expected == result
    assert  expected is not result


@pytest.mark.parametrize("mino_point, centre, expected", [
    (MinoPoint(1, 0), Point(1, 0), MinoPoint(1, 0)),

    (MinoPoint(1, 0), Point(0, 0), MinoPoint(0, 1)),
    (MinoPoint(0, 1), Point(0, 0), MinoPoint(-1, 0)),
    (MinoPoint(-1, 0), Point(0, 0), MinoPoint(0, -1)),
    (MinoPoint(0, -1), Point(0, 0), MinoPoint(1, 0)),

    (MinoPoint(3, 4), Point(1, 2), MinoPoint(-1, 4)),
    (MinoPoint(-1, 4), Point(1, 2), MinoPoint(-1, 0)),
    (MinoPoint(-1, 0), Point(1, 2), MinoPoint(3, 0)),
    (MinoPoint(3, 0), Point(1, 2), MinoPoint(3, 4)),
])
def test_rotate_point_90(mino_point: MinoPoint, centre: Point, expected: MinoPoint):
    assert rotate_point_90(mino_point, centre) == expected
