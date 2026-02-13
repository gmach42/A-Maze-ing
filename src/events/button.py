from typing import Callable
from ..core import XVar, MLXImage
from ..rendering.render_functions import draw_maze_walls


class Button(MLXImage):
    def __init__(
        self,
        xvar: XVar,
        width: int,
        height: int,
        text: str,
        color: int,
        callback: Callable = None,
    ):
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.callback = callback
        super().__init__(xvar, width, height)

    def is_clicked(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= self.x + self.width and
                self.y <= mouse_y <= self.y + self.height)

    def handle_click(self):
        if self.callback:
            self.callback()

    def regen(self, xvar: XVar) -> None:
        self.clear_buffer()
        draw_maze_walls(xvar)

    def reset_draw(self):
        pass