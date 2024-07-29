from threading import Thread
from typing import Optional

from board import Board
from direction import Direction
from piece import Piece


class Engine:

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
    def __init__(self, board: Board):
        self._board = board
        self._background_thread = Thread(target=self._time_passer)
        self._active_piece: Optional[Piece] = None

    def run(self) -> None:
        """
        Runs the game, allowing the user to play
        :return: None
        """
        self._print_instructions()
        self._active_piece = self._board.new_piece()
        print(self._board)
        while True:
            print()
            entry = input("Input a command [L/R/D/DD/U/Q/H]: ")
            alphabet = set("LRDUQHlrduqh")
            alphabet.add("DD")
            alphabet.add("dd")
            if entry not in alphabet:
                print(f"Unsupported input: {entry!r}")
                continue
            entry = entry.upper()
            if entry == "H":
                self._print_instructions()
                continue
            elif entry == "Q":
                print("Quitting...")
                return
            elif entry == "U":
                self._active_piece.rotate()
            elif entry == "DD":
                direction = Direction.DOWN
                while True:
                    shifted = self._active_piece.shift(direction)
                    if not shifted:
                        break
                self._active_piece.declare_frozen()
                self._board.clear_completed_rows()
                self._active_piece = self._board.new_piece()
            else:
                direction = Direction.from_char(entry)
                shifted = self._active_piece.shift(direction)
                if not shifted and direction == Direction.DOWN:
                    self._active_piece.declare_frozen()
                    self._board.clear_completed_rows()
                    self._active_piece = self._board.new_piece()
            print("Board state:")
            print(self._board)

    def _print_instructions(self):
        print(self._INSTRUCTIONS)

    def _time_passer(self) -> None:
        """
        Runs in background, making sure the active piece falls with every second of passing time
        :return: None
        """
        pass