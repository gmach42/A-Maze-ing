from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .xvar import XVar


class MLXImage(ABC):
    """
    Abstract base class representing a drawing surface (MLX Image).

    Defines the interface and common initialization for all visual components
    that manage their own image buffer.

    Attributes:
        img_width (int): Width of the image buffer.
        img_height (int): Height of the image buffer.
        img_ptr (any): Pointer to the MLX image object.
        data (any): Pointer to the raw pixel data buffer.
    """

    def __init__(self, xvar: 'XVar', width: int, height: int):
        """
        Initialize the MLX image buffer.

        Args:
            xvar: The main application state containing the MLX context.
            width: The width of the image in pixels.
            height: The height of the image in pixels.

        Raises:
            RuntimeError: If the MLX image creation fails.
        """
        self.img_width = width
        self.img_height = height

        # Create the MLX image buffer
        self.img_ptr = xvar.mlx.mlx_new_image(xvar.mlx_ptr, width, height)
        if not self.img_ptr:
            raise RuntimeError("Failed to create MLX image")
        res = xvar.mlx.mlx_get_data_addr(self.img_ptr)
        self.data = res[0].cast("I")

    @abstractmethod
    def reset_draw(self, xvar: 'XVar') -> None:
        """
        Reset the image to a blank state. Must be implemented by subclasses.
        """
        pass
