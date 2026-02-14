import array
from ..events import Button
# from mlx import Mlx
from ..core import XVar, MLXImage
from .color_manager import ColorManager
from .animation import draw_maze_walls_anim
from .render_functions import (draw_maze_walls, render_frame_panel,
                               render_frame, display_path)
from ..events.keyboard import (change_maze_color, change_42_color, change_algo,
                               change_solution_color)


class MazeUIManager(MLXImage):

    MIN_PANEL_WIDTH = 300

    def __init__(self,
                 xvar: XVar,
                 width: int,
                 color: ColorManager = ColorManager.SKY):
        self.buttons: list[Button] = [
            Button(xvar, round(width * 0.4), xvar.maze.img_height // 8,
                   "REGENERATE", ColorManager.BLUE, self.regenerate),
            Button(xvar, round(width * 0.4), xvar.maze.img_height // 8,
                   "DISPLAY PATH", ColorManager.BLUE, display_path),
            Button(xvar, round(width * 0.4), xvar.maze.img_height // 8,
                   "CHANGE WALL'S COLOR", ColorManager.BLUE,
                   change_maze_color),
            Button(xvar, round(width * 0.4), xvar.maze.img_height // 8,
                   "CHANGE 42'S COLOR", ColorManager.BLUE, change_42_color),
            Button(xvar, round(width * 0.4), xvar.maze.img_height // 8,
                   "CHANGE ALGO", ColorManager.BLUE, change_algo),
            Button(xvar, round(width * 0.4), xvar.maze.img_height // 8,
                   "CHANGE COLOR PATH", ColorManager.BLUE,
                   change_solution_color)
        ]
        self.color: int = color
        super().__init__(xvar, width, xvar.maze.img_height)

    def add_button(self, xvar: XVar):
        for i, button in enumerate(self.buttons):
            if i < 3:
                offset_x: int = xvar.maze.img_width + (
                    xvar.maze.wall_width) + (xvar.maze.cell_size // 2) + round(
                        self.img_width * 0.08)
                offset_y: int = xvar.maze.cell_size + ((i + 1) *
                                                       (button.height * 2))
            else:
                offset_x = xvar.maze.img_width + (xvar.maze.wall_width) + (
                    xvar.maze.cell_size // 2) + round(self.img_width * 0.52)
                offset_y = xvar.maze.cell_size + (((i + 1) - 3) *
                                                  (button.height * 2))
            button.x = offset_x
            button.y = offset_y
            xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win,
                                             button.img_ptr, offset_x,
                                             offset_y)
            # To be noted that mlx_string_put is in ABGR (Blue <> Red)
            # (Well documented and fonctionning library Mlx is!)
            xvar.mlx.mlx_string_put(
                xvar.mlx_ptr, xvar.win, offset_x +
                round(button.width // 2 - (len(button.text) // 2) * 11),
                offset_y + round(button.height // 2) - 9, ColorManager.GREEN,
                button.text)

    def draw_panel(self, xvar: XVar) -> None:

        x_start: int = 0
        y_start: int = 0
        x_end: int = max(self.img_width - 1, self.MIN_PANEL_WIDTH)
        y_end: int = self.img_height - 1
        draw_width: int = x_end - x_start
        if draw_width <= 0 or y_start >= y_end:
            return

        line_buffer = array.array('I', [self.color] * draw_width)

        for dy in range(y_start, y_end):
            start_offset: int = dy * self.img_width + x_start
            self.data[start_offset:start_offset + draw_width] = line_buffer
        render_frame_panel(xvar, self)
        word: str = 'BIENVENUE SUR A_MAZE_ING!!'
        offset_x: int = xvar.maze.img_width + (xvar.maze.wall_width) + (
            xvar.maze.cell_size // 2)
        offset_y: int = xvar.maze.cell_size
        xvar.mlx.mlx_string_put(
            xvar.mlx_ptr, xvar.win,
            round(self.img_width // 2 - (len(word) // 2) * 11) + offset_x,
            offset_y + round(self.img_height // 8) - 9, ColorManager.BLUE,
            word)
        self.add_button(xvar)

    def regen(self, xvar: XVar) -> None:
        self.reset_draw()
        draw_maze_walls(xvar)

    @staticmethod
    def regenerate(xvar: XVar) -> None:

        xvar.col = 0
        xvar.row = 0
        xvar.maze.reset_draw(xvar)
        xvar.solution.reset_draw()
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
            xvar.solution.draw_solution()
            if xvar.solution.display:
                render_frame(xvar, xvar.solution)

    def reset_draw(self) -> None:
        pass
