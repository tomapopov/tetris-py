import argparse

from board import Board
from engine import Engine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--board_height",
        type=int,
        default=20,
        help="The number of rows that the board should have."
    )
    parser.add_argument(
        "--board_width",
        type=int,
        default=10,
        help="The number of columns that the board should have."
    )
    return parser.parse_args()


def main():
    parsed = parse_args()
    board = Board(parsed.board_height, parsed.board_width)
    engine = Engine(board)
    engine.run()


if __name__ == "__main__":
    main()
