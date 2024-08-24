# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from typing import List

from ..command import Command
from .abstract import Interface
from ..piece import SHAPE_POSSIBILITIES


class InterfaceCLI(Interface):
    _INSTRUCTIONS = """
Welcome to the tetris game. You will be prompted for a command at each step.
The possible commands are:
    1. 'L'  -> Move piece left
    2. 'R'  -> Move piece right
    3. 'D'  -> Move piece down
    4. 'DD' -> Move piece as far down as possible
    5. 'U'  -> Rotate piece 90 degrees clockwise
    6. 'Q'  -> Quit
    7. 'H'  -> Bring up this message again
"""

    def draw_screen(self) -> None:
        """
        Draws the main gameplay screen
        :return: None
        """
        print()
        print(f"SCORE: {self._scorer.score}")
        print(f"LINES CLEARED: {self._scorer.lines_cleared}")
        counts = self._statistics.shape_counts.copy()
        total = sum(counts.values())
        count_strs = [
            (f"{shape.letter}: {counts[shape.letter]} "
             f"({round(0 if total == 0 else counts[shape.letter] / total * 100, 1)}%)")
            for shape in SHAPE_POSSIBILITIES
        ]
        print(f"STATISTICS: {', '.join(count_strs)}")
        print("Board state:")
        print(self._board)
        print()
        print(f"Next Piece: {self._piece_generator.next_piece_type.letter}")

    def get_input(self) -> List[Command]:
        """
        Returns any commands the user has inputted
        :return: list of commands
        """
        try:
            cmd = Command.from_char(input("Input a command [L/R/D/DD/U/Q/H]: "))
        except ValueError:
            return []
        else:
            return [cmd]

    def draw_game_over(self) -> None:
        """
        Draws the end of game screen
        :return: None
        """
        print("GAME OVER")
        print(f"FINAL SCORE: {self._scorer.score}")
        print(f"LINES CLEARED: {self._scorer.lines_cleared}")
        print(f"LEVEL: {self._scorer.level}")

    def show_instructions(self) -> None:
        """
        Shows the instructions to the player
        :return: None
        """
        print(self._INSTRUCTIONS)

    def quit(self) -> None:
        """
        Ends the session
        :return: None
        """
        print("Quitting...")

    def show_paused(self) -> None:
        """
        Shows the user that the game is paused
        :return: None
        """
        pass
