from typing import Callable


class Button:
    def __init__(
        self,
        mlx: object,
        win: int,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        color: int,
        callback: Callable = None,
    ):
        self.mlx = mlx
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.callback = callback

    def is_clicked(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= self.x + self.width and
                self.y <= mouse_y <= self.y + self.height)

    def handle_click(self):
        if self.callback:
            self.callback()
