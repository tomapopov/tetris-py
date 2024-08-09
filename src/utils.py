import argparse


def parse_args() -> argparse.Namespace:
    """
    Parses the command-line args of the game
    :return:
    """
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
