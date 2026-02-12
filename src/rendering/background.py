from ..events import Button


class Background:
    def __init__(self):
        self.buttons = []
        self.title = None


class MazeUIManager:
    def __init__(self, mlx, win):
        self.win = win
        self.mlx = mlx
        self.buttons = []
        self.labels = []

    def add_button(self, button: Button):
        self.buttons.append(button)

    def draw_all(self):
        pass

    def add_label(self):
        pass

    def handle_mouse_click(self):
        pass
