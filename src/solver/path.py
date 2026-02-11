from src.rendering.color_manager import ColorManager
from src.img_data import ImgData, Image
from ..core.xvar import XVar, draw_rectangle, render_frame


class Path(Image):
    def __init__(
        self,
        img_path: ImgData,
        path_matrix: list[tuple[int, int]],
        cell_size: int,
        wall_width: int,
        colors: dict[str, int],
        start: tuple[int, int],
        end: tuple[int, int],
    ):
        self.img_path = img_path
        self.path_matrix = path_matrix
        self.cell_size = cell_size
        self.wall_width = wall_width
        self.colors = colors
        self.start = start
        self.end = end

    def change_color(self, color: int) -> None:
        self.color = color
        # Clear image buffer
        self.img_path.clear_buffer()
        self.regen_path()

    def set_start_end(self, start: tuple[int, int], end: tuple[int, int]
                      ) -> None:
        self.start = start
        self.end = end

    def regen_path(self) -> None:
        self.draw_solution(
            self.img_path,
            self.path_matrix,
            self.color,
            self.cell_size,
            self.wall_width,
        )

    def change_path_color(xvar: XVar):
        color_index = ColorManager.COLOR_LIST.index(xvar.maze.path_color)
        if color_index == len(ColorManager.COLOR_LIST) - 1:
            new_color = ColorManager.WHITE
        else:
            new_color = ColorManager.COLOR_LIST[color_index + 1]
        print("Changing path color to: ", end="")
        print(ColorManager.get_color_name(new_color))

        # Update path with new color
        xvar.maze.change_path_color(new_color)
        render_frame(xvar, xvar.maze.img_maze, xvar.maze.cell_size)

    def draw_solution(self) -> None:
        """Draw the solution path on the maze using `draw_rectangle()`"""
        y_start, x_start = self.path_matrix[0]
        y_end, x_end = self.path_matrix[-1]
        size_path = self.cell_size - self.wall_width
        offset = self.wall_width

        # Draw start
        draw_rectangle(self.img_path, x_start * self.cell_size + offset,
                       y_start * self.cell_size + offset, size_path,
                       size_path, self.colors["start"])

        # Draw end
        draw_rectangle(self.img_path, x_end * self.cell_size + offset, y_end *
                       self.cell_size + offset, size_path, size_path,
                       self.colors["end"])

        # Draw path
        for s in self.path_matrix[1: len(self.path_matrix) - 1]:
            y, x = s
            draw_rectangle(self.img_path, x * self.cell_size + offset, y *
                           self.cell_size + offset, size_path, size_path,
                           self.colors["path"])
