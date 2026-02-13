from ..core import MLXImage, XVar
from .color_manager import ColorManager
from .render_functions import draw_rectangle, render_frame, draw_42


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
        self.end = end,
        self.step: int = 0

    def change_color(self, colors: dict[str, int]) -> None:
        self.colors = colors
        self.regen()

    def set_start_end(
        self,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> None:
        self.start = start
        self.end = end

    def regen(self) -> None:
        self.draw_solution()

    def change_path_color(xvar: XVar):
        color_index = ColorManager.COLOR_LIST.index(
            xvar.solution_path.path_color)
        if color_index == len(ColorManager.COLOR_LIST) - 1:
            new_color = ColorManager.WHITE
        else:
            new_color = ColorManager.COLOR_LIST[color_index + 1]
        print("Changing path color to: ", end="")
        print(ColorManager.get_color_name(new_color))

        xvar.solution_path.change_path_color(new_color)
        render_frame(xvar, xvar.solution_path.img_path,
                     xvar.solution_path.cell_size)

    def draw_solution(self) -> None:
        """Draw the solution path on the maze using `draw_rectangle()`"""
        y_start, x_start = self.path_matrix[0]
        y_end, x_end = self.path_matrix[-1]
        size_path = self.cell_size - self.wall_width
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
        size_path = self.cell_size - self.wall_width
        offset = self.wall_width

        if self.step <= len(self.path_matrix) - 1:
            if self.step == 0:
                color: int = self.colors.get("start")
            elif self.step == len(self.path_matrix) - 1:
                color = self.colors.get("end")
            else:
                color = self.colors.get("path")
            y, x = self.path_matrix[self.step]
            draw_rectangle(self, x * self.cell_size + offset,
                           y * self.cell_size + offset, size_path, size_path,
                           color)
            self.step += 1
            render_frame(xvar, self)
        else:
            xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, None, None)
            # xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, draw_42, xvar)
            draw_42(xvar)

    def reset_draw(self):
        temp = self.colors
        self.colors = {
            'start': ColorManager.BLACK,
            'end': ColorManager.BLACK,
            'path': ColorManager.BLACK,
            }
        self.draw_solution()
        self.colors = temp
