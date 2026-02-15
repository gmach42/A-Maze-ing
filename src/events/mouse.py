from ..core import XVar


def handle_click(mouse_button: int, x: int, y: int, xvar: XVar) -> None:
    """
    Callback function for mouse click events.
    If left mouse_button is clicked inside a button area,
    it calls the button's callback function.
    """
    if mouse_button == 1:
        for element in xvar.manager.buttons:
            if element.is_clicked(x, y):
                element.handle_callable(xvar)
