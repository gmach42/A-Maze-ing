from ..core import XVar


def handle_click(button: int, x: int, y: int, xvar: XVar) -> None:
    if button == 1:
        for element in xvar.manager.buttons:
            if element.is_clicked(x, y):
                element.handle_callable(xvar)
