from board import Board
from engine import Engine
from interface import InterfacePygame
from utils import parse_args


def main():
    parsed = parse_args()
    board = Board(parsed.board_height, parsed.board_width)
    engine = Engine(board, InterfacePygame(board))
    engine.run()


if __name__ == "__main__":
    main()
