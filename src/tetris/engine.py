# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/tomapopov/tetris-py/blob/main/NOTICE

from abc import ABC, abstractmethod
from typing import Optional
import pygame

from .board import Board
from .direction import Direction
from .command import Command
from .piece import Piece, PieceGenerator
from .interface import InterfacePygame, Interface, InterfaceCLI
from .scorer import Scorer
from .statistics import Statistics

_LOOP_SLEEP_TIME_MS = 20


class EngineAbstract(ABC):

    @abstractmethod
    def __init__(self, board: Board, scorer: Scorer, piece_generator: PieceGenerator):
        ...

    @abstractmethod
    def run(self) -> None:
        ...


def parse_direction(key: pygame.key):
    if key == pygame.K_LEFT:
        return Direction.LEFT
    if key == pygame.K_RIGHT:
        return Direction.RIGHT
    if key == pygame.K_DOWN:
        return Direction.DOWN
    raise ValueError(f"Unsupported direction key: {key}")


class Engine(EngineAbstract):
    """
    Generalized engine class used in both versions of the game
    """
    def __init__(self, board: Board, scorer: Scorer, interface: Interface, piece_generator: PieceGenerator, statistics: Statistics):
        self._board = board
        self._piece_generator = piece_generator
        self._interface = interface
        self._active_piece: Optional[Piece] = None
        self._scorer = scorer
        self._statistics = statistics


    def run(self) -> None:
        """
        Runs the game, allowing the user to play
        :return: None
        """
        self._interface.show_instructions()
        self._run_main_loop()
        self._wait(500)
        self._run_game_over_loop()
        self._interface.quit()

    def _run_game_over_loop(self):
        """
        Shows the 'game over' screen until the player exits
        :return: None
        """
        self._interface.draw_game_over()
        show_game_over = True
        while show_game_over:
            cmds = self._interface.get_input()
            for cmd in cmds:
                if cmd == Command.QUIT:
                    show_game_over = False
                    break
            self._wait(_LOOP_SLEEP_TIME_MS)

    def _run_main_loop(self) -> None:
        """
        Runs the main gameplay logic, allowing the user to play until they lose
        :return: None
        """
        self._new_active_piece()
        self._interface.draw_screen()

        # Add timed downwards movement for passage of time
        self._set_downward_movement()

        run = True
        while run:
            need_to_refresh = False
            cmds = self._interface.get_input()
            for cmd in cmds:
                need_to_refresh = True
                if cmd == Command.HELP:
                    self._interface.show_instructions()
                    need_to_refresh = False
                    continue
                elif cmd == Command.QUIT:
                    need_to_refresh = False
                    run = False
                    break
                elif cmd == Command.PAUSE:
                    run = not self._pause()
                    need_to_refresh = run
                elif cmd == Command.ROTATE:
                    self._active_piece.rotate()
                elif cmd == Command.MOVE_BOTTOM:
                    direction = Direction.DOWN
                    while True:
                        shifted = self._active_piece.shift(direction)
                        if not shifted:
                            break
                    lines_cleared = self._board.clear_completed_rows(list(self._active_piece.rows))
                    if lines_cleared > 0:
                        levelled_up = self._scorer.add_to_score(lines_cleared)
                        if levelled_up:
                            # Refresh "falling" logic, to speed it up when needed
                            self._set_downward_movement()
                    if self._board.reached_top_row():
                        # Player has lost
                        run = False
                        break
                    self._new_active_piece()
                    break
                else:
                    direction = Direction.from_command(cmd)
                    self._active_piece.shift(direction)
                    if not self._active_piece.can_shift_down():
                        # Piece is now frozen in place
                        lines_cleared = self._board.clear_completed_rows(list(self._active_piece.rows))
                        if lines_cleared > 0:
                            levelled_up = self._scorer.add_to_score(lines_cleared)
                            if levelled_up:
                                # Refresh "falling" logic, to speed it up when needed
                                self._set_downward_movement()
                        if self._board.reached_top_row():
                            # Player has lost
                            run = False
                            break
                        self._new_active_piece()
                        break

            if need_to_refresh:
                self._interface.draw_screen()

            # Pause to share CPU - not sure if/how much it's needed, haven't
            # looked into the CPU loads yet...
            self._wait(_LOOP_SLEEP_TIME_MS)

    def _new_active_piece(self) -> None:
        """
        Updates the active piece, used when the current piece hits
        the bottom or the stack, and we need a new piece
        :return: None
        """
        self._active_piece = self._board.new_piece(self._piece_generator.generate_new_piece_type())
        self._statistics.inc_count(self._active_piece)

    @abstractmethod
    def _set_downward_movement(self) -> None:
        """
        Sets the automatic downward movement of pieces, so they fall as time passes
        :return: None
        """
        ...

    @abstractmethod
    def _wait(self, time_ms: int) -> None:
        """
        Pauses for a given number of milliseconds
        :param time_ms: time to sleep/wait in millis
        :return: None
        """
        ...

    @abstractmethod
    def _pause(self) -> bool:
        """
        Pauses the game until the pause command is seen again to unpause
        :return: True if quit command was input during pause, False otherwise
        """
        ...


class EnginePygame(Engine):
    _FALL_DELAY = 750

    def __init__(self, board: Board, scorer: Scorer, piece_generator: PieceGenerator, statistics: Statistics):
        super().__init__(board, scorer, InterfacePygame(board, scorer, piece_generator, statistics), piece_generator, statistics)

    def _set_downward_movement(self) -> None:
        """
        Starts the automatic downward movement of pieces, so they fall as time passes
        :return: None
        """
        pygame.time.set_timer(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}), self._FALL_DELAY - self._scorer.level * 50)

    def _wait(self, time_ms: int) -> None:
        """
        Pauses for a given number of milliseconds
        :param time_ms: time to sleep/wait in millis
        :return: None
        """
        pygame.time.wait(time_ms)

    def _pause(self) -> bool:
        """
        Pauses the game until the pause command is seen again to unpause
        :return: True if quit command was input during pause, False otherwise
       """
        self._interface.show_paused()
        while True:
            cmds = self._interface.get_input()
            for cmd in cmds:
                if cmd == Command.PAUSE:
                    return False
                if cmd == Command.QUIT:
                    return True
            pygame.time.wait(50)


class EngineCLI(Engine):

    def __init__(self, board: Board, scorer: Scorer, piece_generator: PieceGenerator, statistics: Statistics):
        super().__init__(board, scorer, InterfaceCLI(board, scorer, piece_generator, statistics), piece_generator, statistics)

    def _set_downward_movement(self) -> None:
        """
        Starts the automatic downward movement of pieces, so they fall as time passes
        :return: None
        """
        pass

    def _wait(self, time_ms: int) -> None:
        """
        Pauses for a given number of milliseconds
        :param time_ms: time to sleep/wait in millis
        :return: None
        """
        pass

    def _pause(self) -> bool:
        """
        Pauses the game until the pause command is seen again to unpause
        :return: True if quit command was input during pause, False otherwise
        """
        return False
