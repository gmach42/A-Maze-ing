from typing import Callable
from ..core import XVar, MLXImage
from ..rendering.render_functions import draw_maze_walls, draw_rectangle


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
        self.x: int = 0
        self.y: int = 0
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.callback = callback
        super().__init__(xvar, width, height)
        draw_rectangle(self, 0, 0, self.width, self.height, self.color)

    def is_clicked(self, mouse_x, mouse_y) -> bool:
        return (self.x <= mouse_x <= self.x + self.width
                and self.y <= mouse_y <= self.y + self.height)

    def handle_callable(self, xvar: XVar) -> None:
        if self.callback:
            self.callback(xvar)

    def regen(self, xvar: XVar) -> None:
        self.clear_buffer()
        draw_maze_walls(xvar)

    def reset_draw(self) -> None:
        pass
