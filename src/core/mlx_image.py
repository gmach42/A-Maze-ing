from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .xvar import XVar


class MLXImage(ABC):
    """Base class for anything that is a drawable MLX image"""

    def __init__(self, xvar: 'XVar', width: int, height: int):
        self.img_width = width
        self.img_height = height

        # Create the MLX image buffer
        self.img_ptr = xvar.mlx.mlx_new_image(xvar.mlx_ptr, width, height)
        if not self.img_ptr:
            raise RuntimeError("Failed to create MLX image")
        res = xvar.mlx.mlx_get_data_addr(self.img_ptr)
        self.data = res[0].cast("I")

    def reset_draw(self, xvar: 'XVar'):
        xvar.mlx.mlx_clear_window(xvar.mlx_ptr, xvar.win)

    @abstractmethod
    def regen(self):
        pass
