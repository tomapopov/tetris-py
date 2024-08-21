from abc import ABC, abstractmethod
from typing import List

import pygame

from .board import Board
from .colours import BLACK_COLOUR, GREY_COLOUR, RED_COLOUR, WHITE_COLOUR, ORANGE_COLOUR
from .piece import PIECE_COLOURS_RGB, PieceGenerator
from .command import Command
from .scorer import Scorer
from .point import MinoPoint


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

    @abstractmethod
    def show_paused(self) -> None:
        """
        Shows the user that the game is paused
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
        print(f"LINES CLEARED: {self._scorer.lines_cleared}")
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


class InterfacePygame(Interface):

    _BLOCK_SCALE_FACTOR = 36
    _WIDTH_PADDING = 40
    _HEIGHT_PADDING = 10
    _INSTRUCTIONS = [
        "← : Move Left",
        "→ : Move Right",
        "↓ : Move Down",
        "↑ : Rotate",
        "<SPC> : Hard Drop",
        "Q : Quit",
        "P : Pause",
    ]
    _font_name = "freesans"
    def __init__(self, *args):
        super().__init__(*args)
        # pygame setup
        pygame.init()
        biggest_screen = sorted(pygame.display.get_desktop_sizes(), reverse=True)[0]
        self._block_size = biggest_screen[1] // self._BLOCK_SCALE_FACTOR

        self._screen_width = (self._board.width + self._WIDTH_PADDING) * self._block_size
        self._screen_height = (self._board.height + self._HEIGHT_PADDING) * self._block_size
        self._screen_size = (self._screen_width, self._screen_height)

        self._grid_width = self._board.width * self._block_size
        self._grid_height = self._board.height * self._block_size
        self._grid_top_left_x = int((self._screen_width - self._grid_width) * 0.50)
        self._grid_top_left_y = (self._screen_height - self._grid_height) // 2

        # Title
        title_label_font_size = int(self._block_size * 1.2)
        title_font = pygame.font.SysFont(self._font_name, title_label_font_size, bold=True)
        self._title_label = title_font.render("TETRIS", 1, WHITE_COLOUR)

        # Game over screen
        self._game_over_label = title_font.render("GAME OVER", 1, RED_COLOUR)

        # Subtitle font, used for score, next piece & pause labels
        subtitle_label_font_size = int(title_label_font_size * 0.6)
        self._subtitle_font = pygame.font.SysFont(self._font_name, subtitle_label_font_size, bold=True)


        # Text Font
        text_font_size = int(title_label_font_size * 0.45)
        self._text_font = pygame.font.SysFont(self._font_name, text_font_size, bold=True)

        # Info Section
        self._info_box_width = self._grid_width
        self._info_box_height = self._grid_height
        self._info_box_top_left_x = int(self._screen_width * 0.75 - self._grid_width // 2)
        self._info_box_top_left_y = self._grid_top_left_y

        self._next_piece_label = self._subtitle_font.render("NEXT PIECE", 1, WHITE_COLOUR)

        self._paused_label = self._subtitle_font.render("PAUSED", 1, ORANGE_COLOUR)
        self._paused_label_top_left_x = self._info_box_top_left_x + self._info_box_width // 2 - self._paused_label.get_width() / 2
        self._paused_label_top_left_y = self._info_box_top_left_y + self._info_box_height - 1.5 * self._block_size

        # Set screen
        self._screen = pygame.display.set_mode(self._screen_size)

    def draw_screen(self) -> None:
        """
        Draws the main gameplay screen
        :return: None
        """
        self._screen.fill(BLACK_COLOUR)
        self._draw_title()
        self._draw_play_grid()
        self._draw_info_section()
        pygame.display.update()

    def _draw_play_grid(self):
        self._draw_tetriminoes()
        self._draw_grid_lines()
        self._draw_border()

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
        instrs_label = self._subtitle_font.render("INSTRUCTIONS", 1, WHITE_COLOUR)
        top_left_x = self._info_box_top_left_x + self._block_size
        instr_top_left_y = self._info_box_top_left_y + self._info_box_height * 0.55
        self._screen.blit(instrs_label,(self._info_box_top_left_x + self._info_box_width / 2 - instrs_label.get_width() / 2, instr_top_left_y))
        sy = instr_top_left_y + instrs_label.get_height() * 1.5
        for i, l in enumerate(self._INSTRUCTIONS):
            top_left_y = sy + self._text_font.get_height() * i * 1.2
            self._text_font.get_height()
            label = self._text_font.render(l, 1, WHITE_COLOUR)
            self._screen.blit(label, (top_left_x, top_left_y))


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

    def show_paused(self) -> None:
        """
        Shows the user that the game is paused
        :return: None
        """

        self._screen.blit(self._paused_label, (self._paused_label_top_left_x, self._paused_label_top_left_y))
        pygame.display.update()

    def _draw_info_section(self) -> None:
        # Border
        pygame.draw.rect(
            surface=self._screen,
            color=GREY_COLOUR,
            rect=(self._info_box_top_left_x, self._info_box_top_left_y, self._info_box_width, self._info_box_height),
            width=1
        )
        self._draw_score_stats()
        self._draw_next_piece_section()
        self.show_instructions()

        # Line above pause box
        pause_box_line_separator_y = self._paused_label_top_left_y - (self._info_box_top_left_y + self._info_box_height - (
                    self._paused_label_top_left_y + self._paused_label.get_height()))
        pygame.draw.line(
            self._screen,
            GREY_COLOUR,
            (self._info_box_top_left_x, pause_box_line_separator_y),
            (self._info_box_top_left_x + self._info_box_width, pause_box_line_separator_y)

        )

    def _draw_score_stats(self) -> None:
        score_label = self._subtitle_font.render(
            f"SCORE: {self._scorer.score}",
            1,
            WHITE_COLOUR,
        )
        lines_label = self._subtitle_font.render(
            f"LINES CLEARED: {self._scorer.lines_cleared}",
            1,
            WHITE_COLOUR,
        )
        level_label = self._subtitle_font.render(
            f"LEVEL: {self._scorer.level}",
            1,
            WHITE_COLOUR,
        )
        top_left_x = self._info_box_top_left_x + self._block_size
        score_top_left_y = self._info_box_top_left_y + self._block_size
        lines_top_left_y = score_top_left_y + self._block_size
        level_top_left_y = lines_top_left_y + self._block_size
        self._screen.blit(score_label, (top_left_x, score_top_left_y))
        self._screen.blit(lines_label, (top_left_x, lines_top_left_y))
        self._screen.blit(level_label, (top_left_x, level_top_left_y))

        sec_separator_line_y = level_top_left_y + level_label.get_height() + score_top_left_y - self._info_box_top_left_y
        pygame.draw.line(
            self._screen,
            GREY_COLOUR,
            (self._info_box_top_left_x, sec_separator_line_y),
            (self._info_box_top_left_x + self._info_box_width, sec_separator_line_y),
        )


    def _draw_next_piece_section(self) -> None:
        label_top_left_x = self._info_box_top_left_x + self._info_box_width // 2 - self._next_piece_label.get_width() / 2
        label_top_left_y = self._info_box_top_left_y + self._block_size * 6
        self._screen.blit(self._next_piece_label, (label_top_left_x, label_top_left_y))

        num_blocks_width = 6
        num_blocks_height = 2
        box_width = num_blocks_width * self._block_size
        box_height = num_blocks_height * self._block_size
        box_top_left_x = label_top_left_x + (self._next_piece_label.get_width() - box_width) / 2
        box_top_left_y = label_top_left_y + self._block_size * 1.5

        pygame.draw.rect(
            surface=self._screen,
            color=GREY_COLOUR,
            rect=(box_top_left_x, box_top_left_y, box_width, box_height),
            width=1
        )
        next_piece_type = self._piece_generator.next_piece_type
        blocks, _ = next_piece_type.points_from_top_left(MinoPoint(2, 0))

        for block in blocks:
            pygame.draw.rect(
                surface=self._screen,
                color=PIECE_COLOURS_RGB[next_piece_type.piece_index],
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

        # TODO: next piece section isn't vertically central in its box right now
        separator_line_y = box_top_left_y + (num_blocks_height + 1) * self._block_size
        pygame.draw.line(
            self._screen,
            GREY_COLOUR,
            (self._info_box_top_left_x, separator_line_y),
            (self._info_box_top_left_x + self._info_box_width, separator_line_y),
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
        score_label = self._subtitle_font.render(f"FINAL SCORE: {self._scorer.score}", 1, WHITE_COLOUR)
        lines_label = self._subtitle_font.render(f"LINES CLEARED: {self._scorer.lines_cleared}", 1, WHITE_COLOUR)
        level_label = self._subtitle_font.render(f"LEVEL: {self._scorer.level}", 1, WHITE_COLOUR)
        self._screen.blit(
            score_label,
            (
                self._screen_width / 2 - (score_label.get_width() / 2),
                self._screen_height * 0.5
            ),
        )
        self._screen.blit(
            lines_label,
            (
                self._screen_width / 2 - (lines_label.get_width() / 2),
                self._screen_height * 0.5 + score_label.get_height() * 1.5,
            ),
        )
        self._screen.blit(
            level_label,
            (
                self._screen_width / 2 - (level_label.get_width() / 2),
                self._screen_height * 0.5 + (lines_label.get_height() + score_label.get_height()) * 1.5,
            ),
        )
