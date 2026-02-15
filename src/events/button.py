from typing import Callable
from ..core import XVar, MLXImage
from ..rendering.render_functions import draw_rectangle


class Button(MLXImage):
    """
    Class to represent a UI button, inheriting from MLXImage.

    Attributes:
        x (int): X-coordinate of the button's top-left corner
        y (int): Y-coordinate of the button's top-left corner
        width (int): Width of the button in pixels
        height (int): Height of the button in pixels
        text (str): Text displayed on the button
        color (int): Color of the button
        callback (Callable[[XVar], None] | None): Function to call when the
            button is clicked
    """

    def __init__(
        self,
        xvar: XVar,
        width: int,
        height: int,
        text: str,
        color: int,
        callback: Callable[[XVar], None] | None = None,
    ):
        """
        Initialize the Button with the given parameters and create the image
        buffer.

        Args:
            xvar (XVar): The main variable containing all necessary data
            width (int): Width of the button in pixels
            height (int): Height of the button in pixels
            text (str): Text to display on the button
            color (int): Color of the button
            callback (Callable[[XVar], None] | None, optional): Function to
                call when the button is clicked. Defaults to None.
        """

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
        """Method to check if the mouse cursor is within the button's area."""
        return (self.x <= mouse_x <= self.x + self.width
                and self.y <= mouse_y <= self.y + self.height)

    def handle_callable(self, xvar: XVar) -> None:
        """
        Handle the button click by calling the assigned callback function.
        """
        if self.callback:
            self.callback(xvar)

    def reset_draw(self, xvar: XVar) -> None:
        pass
