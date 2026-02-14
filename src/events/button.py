from typing import Callable
from ..core import XVar, MLXImage
from ..rendering.render_functions import draw_rectangle


class Button(MLXImage):

    def __init__(
        self,
        xvar: XVar,
        width: int,
        height: int,
        text: str,
        color: int,
        callback: Callable[[XVar], None] | None = None,
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

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        return (self.x <= mouse_x <= self.x + self.width
                and self.y <= mouse_y <= self.y + self.height)

    def handle_callable(self, xvar: XVar) -> None:
        # temp = xvar.manager.buttons
        if self.callback:
            self.callback(xvar)

    def regen(self, xvar: XVar) -> None:
        pass

    def reset_draw(self, xvar: XVar) -> None:
        pass
