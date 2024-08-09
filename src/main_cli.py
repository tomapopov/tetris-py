from src.board import Board
from src.engine import EngineCLI
from src.scorer import SimpleScorer
from src.piece import PieceGenerator
from src.utils import parse_args


def main():
    parsed = parse_args()
    board = Board(parsed.board_height, parsed.board_width)
    scorer = SimpleScorer()
    piece_generator = PieceGenerator()
    engine = EngineCLI(board, scorer, piece_generator)
    engine.run()


if __name__ == "__main__":
    main()
