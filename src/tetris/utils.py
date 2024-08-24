# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

import argparse
from typing import Type, Union

from .board import Board
from .engine import EngineCLI, EnginePygame
from .piece import PieceGenerator
from .scorer import SimpleScorer
from .statistics import Statistics


def parse_args() -> argparse.Namespace:
    """
    Parses the command-line args of the game
    :return:
    """
    parser = argparse.ArgumentParser()
    # Add these later
    # parser.add_argument(
    #     "--board_height",
    #     type=int,
    #     default=20,
    #     help="The number of rows that the board should have."
    # )
    # parser.add_argument(
    #     "--board_width",
    #     type=int,
    #     default=10,
    #     help="The number of columns that the board should have."
    # )
    return parser.parse_args()


def run_game(engine_cls: Type[Union[EngineCLI, EnginePygame]]):
    parsed = parse_args()
    engine = engine_cls()
    engine.run()
