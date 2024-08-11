from abc import ABC, abstractmethod
from typing import Optional
import pygame

from src.board import Board
from src.direction import Direction
from src.command import Command
from src.piece import Piece, PieceGenerator
from src.interface import InterfacePygame, Interface, InterfaceCLI
from src.scorer import Scorer

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
    def __init__(self, board: Board, scorer: Scorer, interface: Interface, piece_generator: PieceGenerator):
        self._board = board
        self._piece_generator = piece_generator
        self._interface = interface
        self._active_piece: Optional[Piece] = None
        self._scorer = scorer

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
        self._start_downward_movement()

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
                    self._pause()
                elif cmd == Command.ROTATE:
                    self._active_piece.rotate()
                elif cmd == Command.MOVE_BOTTOM:
                    direction = Direction.DOWN
                    while True:
                        shifted = self._active_piece.shift(direction)
                        if not shifted:
                            break
                    lines_cleared = self._board.clear_completed_rows()
                    if lines_cleared > 0:
                        self._scorer.add_to_score(lines_cleared, 0)  # level not used right now
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
                        lines_cleared = self._board.clear_completed_rows()
                        if lines_cleared > 0:
                            self._scorer.add_to_score(lines_cleared, 0)  # level not used right now
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

    @abstractmethod
    def _start_downward_movement(self) -> None:
        """
        Starts the automatic downward movement of pieces, so they fall as time passes
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
    def _pause(self) -> None:
        """
        Pauses the game until the pause command is seen again to unpause
        :return: None
        """
        ...




class EnginePygame(Engine):

    def __init__(self, board: Board, scorer: Scorer, piece_generator: PieceGenerator):
        super().__init__(board, scorer, InterfacePygame(board, scorer, piece_generator), piece_generator)

    def _start_downward_movement(self) -> None:
        """
        Starts the automatic downward movement of pieces, so they fall as time passes
        :return: None
        """
        pygame.time.set_timer(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}), 750)

    def _wait(self, time_ms: int) -> None:
        """
        Pauses for a given number of milliseconds
        :param time_ms: time to sleep/wait in millis
        :return: None
        """
        pygame.time.wait(time_ms)

    def _pause(self) -> None:
        """
        Pauses the game until the pause command is seen again to unpause
        :return: None
       """
        self._interface.show_paused()
        while True:
            cmds = self._interface.get_input()
            for cmd in cmds:
                if cmd == Command.PAUSE:
                    return
            pygame.time.wait(50)


class EngineCLI(Engine):

    def __init__(self, board: Board, scorer: Scorer, piece_generator: PieceGenerator):
        super().__init__(board, scorer, InterfaceCLI(board, scorer, piece_generator), piece_generator)

    def _start_downward_movement(self) -> None:
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

    def _pause(self) -> None:
        """
        Pauses the game until the pause command is seen again to unpause
        :return: None
        """
        pass
