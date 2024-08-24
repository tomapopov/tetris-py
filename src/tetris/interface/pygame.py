from typing import Tuple, List

import pygame

from ..colours import YELLOW_COLOUR, WHITE_COLOUR, ORANGE_COLOUR, RED_COLOUR, DARK_GREY_COLOUR, BLACK_COLOUR, \
    GREY_COLOUR
from ..command import Command
from .abstract import Interface
from ..piece import PIECE_COLOURS_RGB, SHAPE_POSSIBILITIES
from ..point import MinoPoint


class PygameButton:

    def __init__(
        self,
        position: Tuple[int, int],
        colour: Tuple,
        hover_colour: Tuple,
        text: pygame.Surface,
        enabled: bool = True,
        border_width: int = 2,
        border_radius: int = 5,
    ):
        self._text = text
        self._position = position
        self._colour = colour
        self._hover_colour = hover_colour
        self._enabled = enabled
        self._width = text.get_width() * 1.3
        self._height = text.get_height() * 1.5
        button_horizontal_middle = self._position[0] + 0.5 * self._width
        button_vertical_middle = self._position[1] + 0.5 * self._height
        self._text_position = (

            button_horizontal_middle - text.get_width() / 2,
            button_vertical_middle - text.get_height() / 2,
        )
        self._rect = pygame.rect.Rect(*self._position, self._width, self._height)
        self._border_width = border_width
        self._border_radius = border_radius

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self._colour, self._rect, width=0, border_radius=self._border_radius)
        pygame.draw.rect(surface, GREY_COLOUR, self._rect, width=self._border_width, border_radius=self._border_radius)  # border
        surface.blit(self._text, self._text_position)


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
        pygame.display.set_caption("Tetris")
        biggest_screen = sorted(pygame.display.get_desktop_sizes(), reverse=True)[0]
        self._block_size = biggest_screen[1] // self._BLOCK_SCALE_FACTOR

        # FONTS
        ## Title font
        title_label_font_size = int(self._block_size * 1.2)
        self._title_font = pygame.font.SysFont(self._font_name, title_label_font_size, bold=False)


        ## Subtitle font
        subtitle_label_font_size = int(title_label_font_size * 0.6)
        self._subtitle_font = pygame.font.SysFont(self._font_name, subtitle_label_font_size, bold=False)

        ## Text Font
        text_font_size = int(title_label_font_size * 0.45)
        self._text_font = pygame.font.SysFont(self._font_name, text_font_size, bold=False)

        # DIMENSIONS
        self._section_width = self._board.width * self._block_size
        self._section_height = self._board.height * self._block_size
        self._section_horizontal_padding = 2 * self._block_size
        self._section_vertical_padding = 4 * self._block_size
        self._section_top_left_y = self._section_vertical_padding

        ## Statistics section
        self._stats_box_width = self._section_width
        self._stats_box_height = self._section_height
        self._stats_box_top_left_x = self._section_horizontal_padding
        self._stats_box_top_left_y = self._section_top_left_y
        self._stats_title = self._title_font.render("STATISTICS", 1, YELLOW_COLOUR)

        ## Play grid section
        self._grid_width = self._board.width * self._block_size
        self._grid_height = self._section_height
        self._grid_top_left_x = self._stats_box_top_left_x + self._stats_box_width + self._section_horizontal_padding
        self._grid_top_left_y = self._section_top_left_y

        ## Info Section
        self._info_box_width = self._grid_width
        self._info_box_height = self._grid_height
        self._info_box_top_left_x = self._grid_top_left_x + self._grid_width + self._section_horizontal_padding
        self._info_box_top_left_y = self._section_top_left_y


        ## Screen Dimensions
        self._screen_width = (self._section_width * 3) + 4 * self._section_horizontal_padding
        # 1.5 vertical padding here for 1 at the top and 0.5 at the bottom of the screen (i.e. less space at the bottom)
        self._screen_height = self._section_height + 1.5 * self._section_vertical_padding
        self._screen_size = (self._screen_width, self._screen_height)

        # LABELS
        self._title_label = self._title_font.render("TETRIS", 1, WHITE_COLOUR)

        self._next_piece_label = self._subtitle_font.render("NEXT PIECE", 1, WHITE_COLOUR)

        self._paused_label = self._subtitle_font.render("PAUSED", 1, ORANGE_COLOUR)
        self._paused_label_top_left_x = self._info_box_top_left_x + self._info_box_width // 2 - self._paused_label.get_width() / 2
        self._paused_label_top_left_y = self._info_box_top_left_y + self._info_box_height - 1.5 * self._block_size

        self._game_over_label = self._title_font.render("GAME OVER", 1, RED_COLOUR)
        # self._restart_button = PygameButton(
        #     (int(self._screen_width * 0.5), int(self._screen_height * 0.8)),
        #     YELLOW_COLOUR,
        #     ORANGE_COLOUR,
        #     self._text_font.render("RESTART", True, BLACK_COLOUR),
        #     enabled=True,
        #     border_width=2,
        #     border_radius=5,
        # )


        # Set screen
        self._screen = pygame.display.set_mode(self._screen_size)

    def draw_screen(self) -> None:
        """
        Draws the main gameplay screen
        :return: None
        """
        self._screen.fill(DARK_GREY_COLOUR)
        self._draw_title()
        self._draw_play_grid()
        self._draw_info_section()
        self._draw_statistics_section()

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
        # Title
        self._screen.blit(
            self._game_over_label,
            (
                self._screen_width / 2 - (self._game_over_label.get_width() / 2),
                self._screen_height * 0.4
            ),
        )
        self._draw_game_over_text()

        # self._restart_button.draw(self._screen)
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
        pygame.quit()

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

        # Minos
        for block in blocks:
            pygame.draw.rect(
                surface=self._screen,
                color=PIECE_COLOURS_RGB[next_piece_type.piece_index],
                rect=(box_top_left_x + block.x * self._block_size, box_top_left_y + block.y * self._block_size, self._block_size, self._block_size),
                width=0,
            )

        # Grid lines
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

    def _draw_statistics_section(self) -> None:
        # Border
        pygame.draw.rect(
            surface=self._screen,
            color=GREY_COLOUR,
            rect=(self._stats_box_top_left_x, self._stats_box_top_left_y, self._stats_box_width, self._stats_box_height),
            width=1
        )

        # Title
        stats_box_middle = self._stats_box_top_left_x + self._stats_box_width / 2
        stats_title_y = self._stats_box_top_left_y + self._block_size * 0.7
        stats_title_x = stats_box_middle - self._stats_title.get_width() / 2
        self._screen.blit(
            self._stats_title,
            (
                stats_title_x,
                stats_title_y,
            )
        )
        line_y = stats_title_y + self._stats_title.get_height() + self._block_size * 0.7
        pygame.draw.line(
            self._screen,
            GREY_COLOUR,
            (self._stats_box_top_left_x, line_y),
            (self._stats_box_top_left_x + self._stats_box_width, line_y),
        )

        # The shape statistics
        spacial_factor = 1.3
        sy = line_y + self._block_size * 0.5
        counts = self._statistics.shape_counts.copy()
        total = sum(counts.values())
        for i, shape in enumerate(SHAPE_POSSIBILITIES):
            letter = shape.letter
            shape_count = counts[letter]
            perc = 0 if total == 0 else round(shape_count / total * 100, 1)
            label = self._title_font.render(f"{letter}: {shape_count} ({perc}%)", 1, PIECE_COLOURS_RGB[shape.piece_index])
            self._screen.blit(
                label,
                (
                    stats_box_middle - label.get_width() / 2,
                    sy + self._title_font.get_height() * spacial_factor * i,
                )
            )

    def _draw_game_over_text(self) -> None:
        score_label = self._subtitle_font.render(f"FINAL SCORE: {self._scorer.score}", 1, WHITE_COLOUR)
        score_label_pos = (
                self._screen_width / 2 - (score_label.get_width() / 2),
                self._screen_height * 0.5
            )
        lines_label = self._subtitle_font.render(f"LINES CLEARED: {self._scorer.lines_cleared}", 1, WHITE_COLOUR)
        lines_label_pos = (
                self._screen_width / 2 - (lines_label.get_width() / 2),
                score_label_pos[1] + score_label.get_height() * 1.5,
            )
        level_label = self._subtitle_font.render(f"LEVEL: {self._scorer.level}", 1, WHITE_COLOUR)
        level_label_pos = (
                self._screen_width / 2 - (level_label.get_width() / 2),
                lines_label_pos[1] + lines_label.get_height() * 1.5,
            )
        self._screen.blit(
            score_label,
            score_label_pos,
        )
        self._screen.blit(
            lines_label,
            lines_label_pos,
        )
        self._screen.blit(
            level_label,
            level_label_pos,
        )
        instrs = self._text_font.render(f"TO START A NEW GAME, PRESS 'R'. TO QUIT, PRESS 'Q'.", 1, YELLOW_COLOUR)
        instrs_pos = (
                self._screen_width / 2 - (instrs.get_width() / 2),
                level_label_pos[1] + level_label.get_height() * 2,
        )
        self._screen.blit(
            instrs,
            instrs_pos,
        )