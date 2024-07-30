from board import Board
from engine import Engine
from interface import InterfacePygame
from scorer import SimpleScorer
from utils import parse_args


def main():
    parsed = parse_args()
    board = Board(parsed.board_height, parsed.board_width)
    scorer = SimpleScorer()
    interface = InterfacePygame(board, scorer)
    engine = Engine(board, interface, scorer)
    engine.run()


if __name__ == "__main__":
    main()
