import array
import random
from ..core import MLXImage, XVar
from ..maze_algorithm import Border
from .color_manager import ColorManager


def draw_rectangle(img_data: MLXImage, x: int, y: int, width: int, height: int,
                   color: int) -> None:
    """
    Main function used to draw in this program.
    It fills a rectangle area in the image data array with a specified color.

    Args:
        img_data (MLXImage): The image data to draw on
        x (int): The x-coordinate of the top-left corner of the rectangle
        y (int): The y-coordinate of the top-left corner of the rectangle
        width (int): The width of the rectangle in pixels
        height (int): The height of the rectangle in pixels
        color (int): The color to fill the rectangle, in ARGB format
    """

    # Secure the rectangle coordinates to be within the image boundaries
    x_start = max(0, x)
    y_start = max(0, y)
    x_end = min(x + width, img_data.img_width)
    y_end = min(y + height, img_data.img_height)

    # If the rectangle is completely outside the image boundaries, do nothing
    draw_width = x_end - x_start
    if draw_width <= 0 or y_start >= y_end:
        return

    # Create a line buffer of the color for improved performance
    line_buffer = array.array("I", [color] * draw_width)

    img_width = img_data.img_width
    data = img_data.data

    # Fill the data array row by row with the line buffer
    for dy in range(y_start, y_end):
        start_offset = dy * img_width + x_start
        data[start_offset:start_offset + draw_width] = line_buffer


def draw_42(xvar: XVar) -> None:
    """Draw the 42 logo on the maze."""

    color: int = ColorManager.BLACK
    # If the maze color is not black, choose a random color for the 42 logo
    # that is different from the maze color
    if xvar.maze.color is not ColorManager.BLACK:
        color = random.choice(
            [col for col in ColorManager.COLOR_LIST if col != xvar.maze.color])
    for row, col in xvar.generator.forty_two_gps:
        y = row * xvar.maze.cell_size
        x = col * xvar.maze.cell_size
        size: int = xvar.maze.cell_size - xvar.maze.wall_width
        draw_rectangle(
            xvar.maze,
            x,
            y,
            xvar.maze.cell_size + xvar.maze.wall_width,
            xvar.maze.wall_width,
            color,
        )
        draw_rectangle(
            xvar.maze,
            x,
            y + xvar.maze.cell_size,
            xvar.maze.cell_size + xvar.maze.wall_width,
            xvar.maze.wall_width,
            color,
        )
        draw_rectangle(
            xvar.maze,
            x,
            y,
            xvar.maze.wall_width,
            xvar.maze.cell_size + xvar.maze.wall_width,
            color,
        )
        draw_rectangle(
            xvar.maze,
            x + xvar.maze.cell_size,
            y,
            xvar.maze.wall_width,
            xvar.maze.cell_size + xvar.maze.wall_width,
            color,
        )
        draw_rectangle(
            xvar.maze,
            x + (xvar.maze.wall_width // 2),
            y + (xvar.maze.wall_width // 2),
            size,
            size,
            color,
        )
        render_frame(xvar, xvar.maze)


def draw_maze_walls(xvar: XVar) -> None:
    """Draw the maze walls based on the maze matrix using `draw_rectangle()`"""

    for row in range(xvar.maze.rows):
        for col in range(xvar.maze.cols):
            cell_value = xvar.maze.maze_matrix[row][col]
            y = row * xvar.maze.cell_size
            x = col * xvar.maze.cell_size
            if cell_value != (Border.NORTH | Border.SOUTH | Border.EAST
                              | Border.WEST):
                if cell_value & Border.NORTH:
                    draw_rectangle(
                        xvar.maze,
                        x,
                        y,
                        xvar.maze.cell_size + xvar.maze.wall_width,
                        xvar.maze.wall_width,
                        xvar.maze.color,
                    )
                if cell_value & Border.SOUTH:
                    draw_rectangle(xvar.maze, x, y + xvar.maze.cell_size,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.wall_width, xvar.maze.color)
                if cell_value & Border.WEST:
                    draw_rectangle(xvar.maze, x, y, xvar.maze.wall_width,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.color)
                if cell_value & Border.EAST:
                    draw_rectangle(
                        xvar.maze,
                        x + xvar.maze.cell_size,
                        y,
                        xvar.maze.wall_width,
                        xvar.maze.cell_size + xvar.maze.wall_width,
                        xvar.maze.color,
                    )
    draw_42(xvar)


def render_frame(xvar: XVar, img_data: MLXImage) -> None:
    """Render the image to the window"""
    offset = xvar.maze.cell_size // 2
    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win, img_data.img_ptr,
                                     offset, offset)


def render_frame_panel(xvar: XVar, img_data: MLXImage) -> None:
    """Render the image to the window"""
    offset: int = xvar.maze.cell_size // 2
    x: int = (offset + xvar.maze.img_width + (xvar.maze.wall_width * 2) + 5)
    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win, img_data.img_ptr,
                                     x, offset)


def display_path(xvar: XVar) -> None:
    """Display the solution path on the maze, with optional animation."""
    if not xvar.solution.display:
        if xvar.animation:
            if xvar.row == xvar.maze.rows:
                xvar.solution.display = True
                xvar.solution.step = 0
                xvar.mlx.mlx_loop_hook(xvar.mlx_ptr,
                                       xvar.solution.draw_solution_anim, xvar)
            else:
                print("Wait until the animation ends")
        else:
            xvar.solution.display = True
            xvar.solution.step = 0
            xvar.solution.draw_solution(xvar)
            render_frame(xvar, xvar.solution)
    else:
        xvar.solution.display = False
        if xvar.solution.step != len(xvar.solution.path_matrix):
            xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, None, None)
        xvar.solution.reset_draw(xvar)
        xvar.solution.step = 0
        render_frame(xvar, xvar.solution)


def render_init(img: MLXImage) -> None:
    """
    Set all pixels of an MLXImage to 0 (transparent) to avoid glitches on
    the first frame.
    """
    draw_rectangle(img, 0, 0, img.img_width, img.img_height, 0)
