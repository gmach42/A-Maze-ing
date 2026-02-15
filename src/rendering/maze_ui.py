import array

from src.parsing.constants import (PANEL_WIDTH, MIN_BUTTON_WIDTH,
                                   MIN_BUTTON_HEIGHT)
from ..events import Button
from ..core import XVar, MLXImage
from .color_manager import ColorManager
from .animation import draw_maze_walls_anim
from .render_functions import (draw_maze_walls, draw_rectangle,
                               render_frame_panel, render_frame, display_path)
from ..events.keyboard import (change_maze_color, change_42_color, change_algo,
                               change_solution_color)


class MazeUIManager(MLXImage):
    """
    Class to manage the UI elements of the maze, inheriting from MLXImage.

    Attributes:
        buttons (list[Button]): List of Button objects representing
            the UI buttons
        color (int): Color used for the panel background
    """

    def __init__(
        self,
        xvar: XVar,
        width: int,
        color: int = ColorManager.PANEL,
        button_color: int = ColorManager.BUTTON,
    ):
        """
        Initialize the MazeUIManager with buttons and panel color.
        Args:
            xvar (XVar): The main variable containing all necessary data
            width (int): The width of the UI panel
            color (int, optional): The background color of the panel.
                Defaults to ColorManager.PANEL.
            button_color (int, optional): The color of the buttons.
                Defaults to ColorManager.BUTTON.
        """
        button_h = max(MIN_BUTTON_HEIGHT, round(xvar.maze.img_height * 0.08))
        button_w = max(MIN_BUTTON_WIDTH, round(width * 0.4))
        self.buttons: list[Button] = [
            Button(xvar, button_w, button_h, "REGENERATE", button_color,
                   self.regenerate),
            Button(xvar, button_w, button_h, "DISPLAY PATH", button_color,
                   display_path),
            Button(xvar, button_w, button_h, "CHANGE WALL'S COLOR",
                   button_color, change_maze_color),
            Button(xvar, button_w, button_h, "CHANGE 42'S COLOR", button_color,
                   change_42_color),
            Button(xvar, button_w, button_h, "CHANGE ALGO", button_color,
                   change_algo),
            Button(xvar, button_w, button_h, "CHANGE COLOR PATH", button_color,
                   change_solution_color)
        ]
        self.color: int = color
        super().__init__(xvar, width, xvar.maze.img_height)

    def add_button(self, xvar: XVar) -> None:
        """Add a button to the UI panel and display it."""
        for i, button in enumerate(self.buttons):
            if i < 3:
                offset_x: int = xvar.maze.img_width + xvar.maze.wall_width + \
                    xvar.maze.cell_size + round(self.img_width * 0.08)
                offset_y: int = xvar.maze.cell_size // 2 + (
                    (i + 1) * round(0.25 * self.img_height))
            else:
                offset_x = xvar.maze.img_width + xvar.maze.wall_width + (
                    xvar.maze.cell_size) + round(self.img_width * 0.52)
                offset_y = xvar.maze.cell_size // 2 + ((
                    (i + 1) - 3) * round(0.25 * self.img_height))
            button.x = offset_x
            button.y = offset_y
            xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win,
                                             button.img_ptr, offset_x,
                                             offset_y)
            # To be noted that mlx_string_put is in ABGR (Blue <> Red)
            # (Well documented and fonctionning library Mlx is!)
            text_x = offset_x + button.width // 2 - (len(button.text) //
                                                     2) * 11
            xvar.mlx.mlx_string_put(xvar.mlx_ptr, xvar.win, text_x,
                                    offset_y + round(button.height // 2) - 9,
                                    ColorManager.CYAN, button.text)

    def draw_panel(self, xvar: XVar) -> None:
        """Draw the UI panel background and decorative elements."""

        x_start: int = 0
        y_start: int = 0
        x_end: int = PANEL_WIDTH
        y_end: int = self.img_height - 1
        draw_width: int = x_end - x_start
        if draw_width <= 0 or y_start >= y_end:
            return

        line_buffer = array.array('I', [self.color] * draw_width)

        for dy in range(y_start, y_end):
            start_offset: int = dy * self.img_width + x_start
            self.data[start_offset:start_offset + draw_width] = line_buffer

        word: str = 'BIENVENUE SUR A_MAZE_ING!!'
        offset_x: int = xvar.maze.img_width + xvar.maze.wall_width + \
            xvar.maze.cell_size
        offset_y: int = round(
            0.25 * self.img_height) // 2 + xvar.maze.cell_size // 2

        # Decorative lines for the welcome message
        draw_rectangle(
            self, round(self.img_width * 0.2),
            offset_y - xvar.maze.cell_size // 2 - self.img_height // 20,
            round(self.img_width * 0.6), 10, ColorManager.BUTTON)
        draw_rectangle(
            self, round(self.img_width * 0.2),
            offset_y - xvar.maze.cell_size // 2 + self.img_height // 20,
            round(self.img_width * 0.6), 10, ColorManager.BUTTON)

        render_frame_panel(xvar, self)

        # RED and BLUE inversed -> mlx_string_put is in ABGR (Blue <> Red)
        text_x = offset_x + self.img_width // 2 - (len(word) // 2) * 10
        xvar.mlx.mlx_string_put(xvar.mlx_ptr, xvar.win, text_x, offset_y - 7,
                                ColorManager.CYAN, word)

        self.add_button(xvar)

    @staticmethod
    def regenerate(xvar: XVar) -> None:
        """
        Major function to regenerate the maze and
        update the display accordingly.
        """

        xvar.col = 0
        xvar.row = 0
        xvar.maze.reset_draw(xvar)
        xvar.solution.reset_draw(xvar)
        render_frame(xvar, xvar.solution)
        xvar.solution.step = 0
        xvar.maze.maze_matrix = xvar.generator.get_maze()
        xvar.solver.maze = xvar.maze.maze_matrix
        xvar.solution.path_matrix = xvar.solver.a_star_algorithm()
        if xvar.animation:
            xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, draw_maze_walls_anim, xvar)
        else:
            draw_maze_walls(xvar)
            render_frame(xvar, xvar.maze)
            xvar.solution.draw_solution(xvar)
            if xvar.solution.display:
                render_frame(xvar, xvar.solution)

    def reset_draw(self, xvar: XVar) -> None:
        pass
