import array
from ..events import Button
# from mlx import Mlx
from ..core import XVar, MLXImage
from .color_manager import ColorManager
from .render_functions import draw_maze_walls, render_frame_panel


class Background:

    def __init__(self):
        self.buttons = []
        self.title = None


class MazeUIManager(MLXImage):

    def __init__(self,
                 xvar: XVar,
                 color: ColorManager = ColorManager.SKY):
        self.buttons = []
        self.labels = []
        self.color: int = color
        super().__init__(xvar, 290, xvar.maze.img_height)

    def add_button(self, button: Button):
        self.buttons.append(button)

    def draw_all(self):
        pass

    def add_label(self):
        pass

    def handle_mouse_click(self):
        pass

    def draw_panel(self, xvar: XVar):

        x_start: int = 0
        y_start: int = 0
        x_end: int = self.img_width
        y_end: int = self.img_height
        draw_width: int = x_end - x_start
        if draw_width <= 0 or y_start >= y_end:
            return

        line_buffer = array.array('I', [self.color] * draw_width)

        for dy in range(y_start, y_end):
            start_offset: int = dy * self.img_width + x_start
            self.data[start_offset:start_offset + draw_width] = line_buffer
        render_frame_panel(xvar, self)

    def regen(self, xvar: XVar) -> None:
        self.clear_buffer()
        draw_maze_walls(xvar)
