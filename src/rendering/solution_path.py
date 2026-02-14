from ..core import MLXImage, XVar
from .color_manager import ColorManager
from .render_functions import draw_rectangle, render_frame


class SolutionPath(MLXImage):

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
        self.colors = colors
        self.regen(xvar)

    def set_start_end(self, start: tuple[int, int], end: tuple[int,
                                                               int]) -> None:
        self.start = start
        self.end = end

    def regen(self, xvar: XVar) -> None:
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
        """Draw the solution path on the maze using `draw_rectangle()`"""
        self.display = True
        size_path = self.cell_size - self.wall_width
        offset = self.wall_width

        if self.step <= len(self.path_matrix) - 1:
            if self.step == 0:
                color: int = self.colors.get("start", 0xFFFF0000)
            elif self.step == len(self.path_matrix) - 1:
                color = self.colors.get("end", 0xFF00FF00)
            else:
                color = self.colors.get("path", 0xFF0000FF)
            y, x = self.path_matrix[self.step]
            draw_rectangle(self, x * self.cell_size + offset,
                           y * self.cell_size + offset, size_path, size_path,
                           color)
            self.step += 1
            render_frame(xvar, self)
        else:
            xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, None, None)

    def reset_draw(self, xvar: XVar) -> None:
        temp_colors: dict[str, int] = self.colors
        self.colors = {
            'start': ColorManager.BLACK,
            'end': ColorManager.BLACK,
            'path': ColorManager.BLACK,
        }
        self.draw_solution(xvar)
        self.colors = temp_colors
