from abc import ABC, abstractmethod
from typing import List

import pygame

from board import Board
from colours import BLACK_COLOUR, GREY_COLOUR
from piece import PIECE_COLOURS_RGB
from command import Command


class Interface(ABC):

    def __init__(self, board: Board):
        self._board = board

    @abstractmethod
    def get_input(self) -> List[Command]:
        ...

    @abstractmethod
    def draw_screen(self) -> None:
        ...

    @abstractmethod
    def show_instructions(self) -> None:
        ...

    @abstractmethod
    def quit(self) -> None:
        ...


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
        print()
        print("Board state:")
        print(self._board)
        print()

    def show_instructions(self) -> None:
        print(self._INSTRUCTIONS)

    def get_input(self) -> List[Command]:
        try:
            cmd = Command.from_char(input("Input a command [L/R/D/DD/U/Q/H]: "))
        except ValueError:
            return []
        else:
            return [cmd]

    def quit(self) -> None:
        print("Quitting...")

class InterfacePygame(Interface):

    def __init__(self, board):
        super().__init__(board)
        # pygame setup
        pygame.init()
        self._block_size = 30
        self._padding = 10
        self._play_width = self._board.width * self._block_size
        self._play_height = self._board.height * self._block_size
        self._screen_size = (
            (self._board.width + self._padding) * self._block_size,
            (self._board.height + self._padding) * self._block_size
        )
        self._grid_top_left_x = (self._screen_size[0] - self._play_width) // 2
        self._grid_top_left_y = (self._screen_size[1] - self._play_height) // 2
        self._screen = pygame.display.set_mode(self._screen_size)

    def get_input(self) -> List[Command]:
        events = pygame.event.get()
        cmds = []
        for event in events:
            ev_type = event.type
            if ev_type == pygame.QUIT:
                cmds.append(Command.QUIT)
                break
            elif ev_type == pygame.KEYDOWN:
                try:
                    cmd = Command.from_pygame_key(event.key)
                except ValueError:
                    continue
                else:
                    cmds.append(cmd)
                    if cmd is Command.QUIT:
                        break
        return cmds

    def draw_screen(self) -> None:
        self._screen.fill(BLACK_COLOUR)
        # Tetris Title
        font = pygame.font.SysFont("comicsans", 60)
        label = font.render("TETRIS", 1, (255,255,255))
        self._screen.blit(label, (self._screen_size[0] / 2 - (label.get_width() / 2), self._block_size))

        self._draw_tetriminoes()
        self._draw_grid_lines()
        self._draw_border()
        pygame.display.update()

    def _draw_tetriminoes(self):
        sx = self._grid_top_left_x
        sy = self._grid_top_left_y
        for i in range(self._board.height):
            for j in range(self._board.width):
                pygame.draw.rect(
                    surface=self._screen,
                    color=PIECE_COLOURS_RGB[self._board._grid[i][j]],
                    rect=(sx + j * self._block_size, sy + i * self._block_size, self._block_size, self._block_size),
                    width=0,
                )

    def _draw_grid_lines(self) -> None:
        """
        Draws the grey grid lines that we see
        :return: None
        """
        sx = self._grid_top_left_x
        sy = self._grid_top_left_y
        for i in range(self._board.height):
            pygame.draw.line(
                self._screen,
                GREY_COLOUR,
                (sx, sy + i * self._block_size),
                (sx + self._play_width, sy + i * self._block_size),
            )  # horizontal lines
            for j in range(self._board.width):
                pygame.draw.line(
                    self._screen,
                    GREY_COLOUR,
                    (sx + j * self._block_size, sy),
                    (sx + j * self._block_size, sy + self._play_height),
                )  # vertical line

    def _draw_border(self) -> None:
        sx = self._grid_top_left_x
        sy = self._grid_top_left_y
        pygame.draw.rect(surface=self._screen, color=(255, 0, 0), rect=(sx, sy, self._play_width, self._play_height), width=5)

    def show_instructions(self) -> None:
        pass  # TODO

    def quit(self) -> None:
        pygame.display.quit()
