import array
from ..events import Button
# from mlx import Mlx
from ..core import XVar, MLXImage
from .color_manager import ColorManager
from .solution_path import SolutionPath
from .animation import draw_maze_walls_anim
from .render_functions import (draw_maze_walls, render_frame_panel,
                               render_frame, display_path)
from ..events.keyboard import change_maze_color


class MazeUIManager(MLXImage):

    def __init__(self,
                 xvar: XVar,
                 width: int,
                 color: ColorManager = ColorManager.SKY):
        self.buttons = [
            Button(xvar, round(width * 0.8), xvar.maze.img_height // 4,
                   "Regenerate", ColorManager.BLUE, self.regenerate),
            Button(xvar, round(width * 0.8), xvar.maze.img_height // 4,
                   "Display path", ColorManager.BLUE, display_path),
            Button(xvar, round(width * 0.8), xvar.maze.img_height // 4,
                   "Change wall's color", ColorManager.BLUE,
                   change_maze_color),
            Button(xvar, round(width * 0.8), xvar.maze.img_height // 4,
                   "Change 42's color", ColorManager.BLUE, display_path)
        ]
        self.labels = []
        self.color: int = color
        super().__init__(xvar, width, xvar.maze.img_height)
        print(width)

    def add_button(self, button: Button):
        self.buttons.append(button)

    def draw_all(self):
        pass

    def add_label(self, xvar: XVar, x: int, y: int, color: int, txt: str):
        xvar.mlx.mlx_string_put(xvar.mlx_ptr, xvar.mlx.win, x, y, color, txt)

    def handle_mouse_click(self):
        pass

    def draw_panel(self, xvar: XVar):

        x_start: int = 0
        y_start: int = 0
        x_end: int = self.img_width - 1
        y_end: int = self.img_height - 1
        draw_width: int = x_end - x_start
        if draw_width <= 0 or y_start >= y_end:
            return

        line_buffer = array.array('I', [self.color] * draw_width)

        for dy in range(y_start, y_end):
            start_offset: int = dy * self.img_width + x_start
            self.data[start_offset:start_offset + draw_width] = line_buffer
        render_frame_panel(xvar, self)

    def regen(self, xvar: XVar) -> None:
        self.reset_draw()
        draw_maze_walls(xvar)

    @staticmethod
    def regenerate(xvar: XVar):
        xvar.maze.reset_draw(xvar)
        xvar.solution.reset_draw()
        xvar.maze.maze_matrix = xvar.generator.get_maze()
        xvar.solver.maze = xvar.maze.maze_matrix
        xvar.solution.path_matrix = xvar.solver.a_star_algorithm()
        if xvar.animation:
            xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, draw_maze_walls_anim, xvar)
        else:
            draw_maze_walls(xvar)
            render_frame(xvar, xvar.maze)
            xvar.solution.draw_solution()
            render_frame(xvar, xvar.solution)

    def reset_draw(self):
        pass
