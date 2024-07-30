from abc import ABC, abstractmethod
from typing import Optional
import pygame

from board import Board
from direction import Direction
from command import Command
from piece import Piece
from interface import InterfacePygame, Interface
from scorer import Scorer


class EngineAbstract(ABC):

    @abstractmethod
    def __init__(self, board: Board):
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


class EnginePygame(EngineAbstract):
    """
    TODO: not used atm but may need to once implementing clock logic
    """
    def __init__(self, board: Board):
        self._board = board
        self._active_piece: Optional[Piece] = None
        self._interface = InterfacePygame(board)
        self._clock = pygame.time.Clock()

    def run(self) -> None:
        self._active_piece = self._board.new_piece()
        self._interface.draw_screen()
        run = True
        while run:
            events = pygame.event.get()
            print(len(events), events)
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_UP:
                        self._active_piece.rotate()
                    elif key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN):
                        direction = parse_direction(key)
                        self._active_piece.shift(direction)
                        if not self._active_piece.can_shift_down():
                            # Piece is now frozen in place
                            self._board.clear_completed_rows()
                            self._active_piece = self._board.new_piece()
            self._interface.draw_screen()


        pygame.display.quit()
        quit()


class Engine(EngineAbstract):
    """
    Generalized engine class used in both versions of the game
    """
    def __init__(self, board: Board, interface: Interface, scorer: Scorer):
        self._board = board
        self._interface = interface
        self._active_piece: Optional[Piece] = None
        self._scorer = scorer

    def run(self) -> None:
        """
        Runs the game, allowing the user to play
        :return: None
        """
        self._interface.show_instructions()
        self._active_piece = self._board.new_piece()
        self._interface.draw_screen()
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
                    self._active_piece = self._board.new_piece()
                else:
                    direction = Direction.from_command(cmd)
                    self._active_piece.shift(direction)
                    if not self._active_piece.can_shift_down():
                        # Piece is now frozen in place
                        lines_cleared = self._board.clear_completed_rows()
                        if lines_cleared > 0:
                            self._scorer.add_to_score(lines_cleared, 0)  # level not used right now
                        self._active_piece = self._board.new_piece()
            if need_to_refresh:
                self._interface.draw_screen()
        self._interface.quit()
