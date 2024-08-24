# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from abc import ABC, abstractmethod
from typing import List

from ..board import Board
from ..piece import PieceGenerator
from ..command import Command
from ..scorer import Scorer
from ..statistics import Statistics


class Interface(ABC):

    def __init__(self, board: Board, scorer: Scorer, piece_generator: PieceGenerator,  statistics: Statistics):
        self._board = board
        self._scorer = scorer
        self._piece_generator = piece_generator
        self._statistics = statistics

    @abstractmethod
    def draw_screen(self) -> None:
        """
        Draws the main gameplay screen
        :return: None
        """
        ...

    @abstractmethod
    def get_input(self) -> List[Command]:
        """
        Returns any commands the user has inputted
        :return: list of commands
        """
        ...

    @abstractmethod
    def draw_game_over(self) -> None:
        """
        Draws the end of game screen
        :return: None
        """
        ...

    @abstractmethod
    def show_instructions(self) -> None:
        """
        Shows the instructions to the player
        :return: None
        """
        ...

    @abstractmethod
    def quit(self) -> None:
        """
        Ends the session
        :return: None
        """
        ...

    @abstractmethod
    def show_paused(self) -> None:
        """
        Shows the user that the game is paused
        :return: None
        """
        ...
