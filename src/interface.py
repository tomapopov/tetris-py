from abc import ABC, abstractmethod
from typing import List

import pygame

from board import Board
from colours import BLACK_COLOUR, GREY_COLOUR, RED_COLOUR, WHITE_COLOUR
from piece import PIECE_COLOURS_RGB, PieceGenerator
from command import Command
from scorer import Scorer
from point import MinoPoint


class Interface(ABC):

    def __init__(self, board: Board, scorer: Scorer, piece_generator: PieceGenerator):
        self._board = board
        self._scorer = scorer
        self._piece_generator = piece_generator

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
        print("Board state:")
        print(self._board)
        print()
        print(f"Next Piece: {self._piece_generator.next_piece_type}")

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


class InterfacePygame(Interface):

    def __init__(self, *args):
        super().__init__(*args)
        # pygame setup
        pygame.init()
        self._block_size = 30
        self._width_padding = 20
        self._height_padding = 10

        self._screen_width = (self._board.width + self._width_padding) * self._block_size
        self._screen_height =  (self._board.height + self._height_padding) * self._block_size
        self._screen_size = (self._screen_width, self._screen_height)

        self._grid_width = self._board.width * self._block_size
        self._grid_height = self._board.height * self._block_size
        self._grid_top_left_x = int((self._screen_width - self._grid_width) * 0.25)
        self._grid_top_left_y = (self._screen_height - self._grid_height) // 2

        font = pygame.font.SysFont("comicsans", 60)
        self._title_label = font.render("TETRIS", 1, WHITE_COLOUR)

        self._game_over_label = font.render("GAME OVER", 1, RED_COLOUR)

        self._screen = pygame.display.set_mode(self._screen_size)

    def draw_screen(self) -> None:
        """
        Draws the main gameplay screen
        :return: None
        """
        self._screen.fill(BLACK_COLOUR)
        self._draw_title()
        self._draw_tetriminoes()
        self._draw_grid_lines()
        self._draw_border()
        self._draw_score()
        self._draw_next_piece()
        pygame.display.update()

    def get_input(self) -> List[Command]:
        """
        Returns any commands the user has inputted
        :return: list of commands
        """
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

    def draw_game_over(self) -> None:
        """
        Draws the end of game screen
        :return: None
        """
        self._screen.fill(BLACK_COLOUR)
        self._draw_game_over_title()
        self._draw_final_score()
        pygame.display.update()

    def show_instructions(self) -> None:
        """
        Shows the instructions to the player
        :return: None
        """
        pass  # TODO: Not implemented yet

    def quit(self) -> None:
        """
        Ends the session
        :return: None
        """
        pygame.display.quit()

    def _draw_title(self) -> None:
        self._screen.blit(
            self._title_label,
            (
                self._screen_width / 2 - (self._title_label.get_width() / 2),
                self._block_size,
            ),
        )

    def _draw_game_over_title(self) -> None:
        self._screen.blit(
            self._game_over_label,
            (
                self._screen_width / 2 - (self._game_over_label.get_width() / 2),
                self._screen_height * 0.4
            ),
        )

    def _draw_final_score(self) -> None:
        font = pygame.font.SysFont("comicsans", 40)
        label = font.render(f"FINAL SCORE: {self._scorer.score}", 1, WHITE_COLOUR)
        self._screen.blit(
            label,
            (
                self._screen_width / 2 - (label.get_width() / 2),
                self._screen_height * 0.5
            ),
        )

    def _draw_tetriminoes(self):
        sx = self._grid_top_left_x
        sy = self._grid_top_left_y
        for i in range(self._board.height):
            for j in range(self._board.width):
                pygame.draw.rect(
                    surface=self._screen,
                    color=PIECE_COLOURS_RGB[self._board.value_at(i, j)],
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
                (sx + self._grid_width - 1, sy + i * self._block_size),
            )  # horizontal lines
            for j in range(self._board.width):
                pygame.draw.line(
                    self._screen,
                    GREY_COLOUR,
                    (sx + j * self._block_size, sy),
                    (sx + j * self._block_size, sy + self._grid_height - 1),
                )  # vertical line

    def _draw_border(self) -> None:
        sx = self._grid_top_left_x
        sy = self._grid_top_left_y
        pygame.draw.rect(surface=self._screen, color=RED_COLOUR, rect=(sx, sy, self._grid_width, self._grid_height), width=2)

    def _draw_score(self) -> None:
        font = pygame.font.SysFont("comicsans", 40)
        label = font.render(f"SCORE: {self._scorer.score}", 1, (255, 255, 255))
        score_top_left_x = (self._grid_top_left_x + self._grid_width / 2) - label.get_width() / 2
        score_top_left_y = self._grid_top_left_y - self._block_size
        self._screen.blit(label, (score_top_left_x, score_top_left_y))

    def _draw_next_piece(self) -> None:
        font = pygame.font.SysFont("comicsans", 40)
        label = font.render("NEXT PIECE", 1, (255, 255, 255))
        label_top_left_x = self._screen_width * 0.75 - label.get_width() / 2
        label_top_left_y = self._screen_height * 0.3

        num_blocks_width = 6
        num_blocks_height = 2
        box_width = num_blocks_width * self._block_size
        box_height = num_blocks_height * self._block_size
        box_top_left_x = label_top_left_x + (label.get_width() - box_width) / 2
        box_top_left_y = label_top_left_y + self._block_size * 2

        pygame.draw.rect(
            surface=self._screen,
            color=GREY_COLOUR,
            rect=(box_top_left_x, box_top_left_y, box_width, box_height),
            width=1
        )
        next_piece_type = self._piece_generator.next_piece_type
        # TODO: shouldn't be calling init state here, should extract relevant info into another method
        blocks, centre = next_piece_type.init_state(MinoPoint(2, 0))

        for block in blocks:
            pygame.draw.rect(
                surface=self._screen,
                color=PIECE_COLOURS_RGB[next_piece_type.colour_code],
                rect=(box_top_left_x + block.x * self._block_size, box_top_left_y + block.y * self._block_size, self._block_size, self._block_size),
                width=0,
            )

        for i in range(num_blocks_height):
            pygame.draw.line(
                self._screen,
                GREY_COLOUR,
                (box_top_left_x, box_top_left_y + i * self._block_size),
                (box_top_left_x + box_width, box_top_left_y + i * self._block_size),
            )  # horizontal lines
            for j in range(num_blocks_width):
                pygame.draw.line(
                    self._screen,
                    GREY_COLOUR,
                    (box_top_left_x + j * self._block_size, box_top_left_y),
                    (box_top_left_x + j * self._block_size, box_top_left_y + box_height),
                )  # vertical line

        self._screen.blit(label, (label_top_left_x, label_top_left_y))
