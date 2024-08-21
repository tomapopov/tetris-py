from .board import Board
from .engine import EnginePygame
from .scorer import SimpleScorer
from .piece import PieceGenerator
from .utils import parse_args


def main():
    parsed = parse_args()
    board = Board(parsed.board_height, parsed.board_width)
    scorer = SimpleScorer()
    piece_generator = PieceGenerator()
    engine = EnginePygame(board, scorer, piece_generator)
    engine.run()


if __name__ == "__main__":
    main()
