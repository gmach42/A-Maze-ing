from ..core import XVar


def handle_click(button: int, x: int, y: int, xvar: XVar) -> None:
    if button == 1:
        for button in xvar.manager.buttons:
            if button.is_clicked(x, y):
                button.handle_callable(xvar)
