from ..core import MLXImage, XVar
from .color_manager import ColorManager
from .render_functions import draw_rectangle, render_frame


class SolutionPath(MLXImage):
    """
    Class to represent the solution path of the maze, inheriting from MLXImage.

    Attributes:
        path_matrix (list[tuple[int, int]]): List of coordinates representing
            the solution path
        cell_size (int): Size of each cell in pixels
        wall_width (int): Width of the walls in pixels
        colors (dict[str, int]): Dictionary of colors for start, end, and path
        start (tuple[int, int]): Coordinates of the start cell
        end (tuple[int, int]): Coordinates of the end cell
        step (int): Current step in the animation
        display (bool): Flag to indicate if the solution should be displayed
    """

    def __init__(
        self,
        xvar: XVar,
        rows: int,
        cols: int,
        path_matrix: list[tuple[int, int]],
        wall_width: int,
        colors: dict[str, int],
        start: tuple[int, int],
        end: tuple[int, int],
        cell_size: int,
    ):
        """
        Initialize the SolutionPath with the given parameters and create the
        image buffer.

        Args:
            xvar (XVar): The main variable containing all necessary data
            rows (int): Number of rows in the maze
            cols (int): Number of columns in the maze
            path_matrix (list[tuple[int, int]]): List of coordinates
                representing the solution path
            wall_width (int): Width of the walls in pixels
            colors (dict[str, int]): Dictionary of colors for start, end, and
                path
        """
        pixel_width = cols * cell_size + wall_width + 1
        pixel_height = rows * cell_size + wall_width + 1

        super().__init__(xvar, pixel_width, pixel_height)

        self.path_matrix = path_matrix
        self.cell_size = cell_size
        self.wall_width = wall_width
        self.colors = colors
        self.start = start
        self.end = end
        self.step: int = 0
        self.display: bool = False

    def change_color(self, colors: dict[str, int], xvar: XVar) -> None:
        """Change the colors used for the solution path and redraw it."""
        self.colors = colors
        self.regen(xvar)

    def set_start_end(self, start: tuple[int, int], end: tuple[int,
                                                               int]) -> None:
        """Setter for start and end coordinates."""
        self.start = start
        self.end = end

    def regen(self, xvar: XVar) -> None:
        """Redraw the solution path."""
        self.draw_solution(xvar)

    def draw_solution(self, xvar: XVar) -> None:
        """Draw the solution path on the maze using `draw_rectangle()`"""
        y_start, x_start = self.path_matrix[0]
        y_end, x_end = self.path_matrix[-1]
        size_path = xvar.maze.cell_size - self.wall_width
        offset = self.wall_width

        # Draw start
        draw_rectangle(self, x_start * self.cell_size + offset,
                       y_start * self.cell_size + offset, size_path, size_path,
                       self.colors["start"])

        # Draw end
        draw_rectangle(self, x_end * self.cell_size + offset,
                       y_end * self.cell_size + offset, size_path, size_path,
                       self.colors["end"])

        # Draw path
        for s in self.path_matrix[1:len(self.path_matrix) - 1]:
            y, x = s
            draw_rectangle(self, x * self.cell_size + offset,
                           y * self.cell_size + offset, size_path, size_path,
                           self.colors["path"])

    def draw_solution_anim(self, xvar: XVar) -> None:
        """
        Draw an animation of the solution path on the maze with default colors.
        """
        self.display = True
        size_path = self.cell_size - self.wall_width
        offset = self.wall_width

        if self.step <= len(self.path_matrix) - 1:
            if self.step == 0:
                color: int = self.colors.get("start", ColorManager.START)
            elif self.step == len(self.path_matrix) - 1:
                color = self.colors.get("end", ColorManager.END)
            else:
                color = self.colors.get("path", ColorManager.PATH)
            y, x = self.path_matrix[self.step]
            draw_rectangle(self, x * self.cell_size + offset,
                           y * self.cell_size + offset, size_path, size_path,
                           color)
            self.step += 1
            render_frame(xvar, self)
        else:
            xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, None, None)

    def reset_draw(self, xvar: XVar) -> None:
        """Erase the solution path by drawing it with black color."""
        temp_colors: dict[str, int] = self.colors
        self.colors = {
            'start': ColorManager.BLACK,
            'end': ColorManager.BLACK,
            'path': ColorManager.BLACK,
        }
        self.draw_solution(xvar)
        self.colors = temp_colors
