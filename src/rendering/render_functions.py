import array
from ..core import MLXImage, XVar
from ..maze_algorithm import Border


def draw_rectangle(img_data: MLXImage, x: int, y: int, width: int, height: int,
                   color: int) -> None:
    """Draw a filled rectangle"""
    x_start = max(0, x)
    y_start = max(0, y)
    x_end = min(x + width, img_data.img_width)
    y_end = min(y + height, img_data.img_height)

    draw_width = x_end - x_start
    if draw_width <= 0 or y_start >= y_end:
        return

    line_buffer = array.array('I', [color] * draw_width)

    img_width = img_data.img_width
    data = img_data.data

    for dy in range(y_start, y_end):
        start_offset = dy * img_width + x_start
        data[start_offset:start_offset + draw_width] = line_buffer


def draw_maze_walls(
    img_data: MLXImage,
    maze: list[list[int]],
    cell_size: int,
    wall_width: int,
    color: int,
) -> None:
    """Draw walls around each cell"""
    rows = len(maze)
    cols = len(maze[0])

    for row in range(rows):
        for col in range(cols):
            cell_value = maze[row][col]
            x = col * cell_size
            y = row * cell_size

            if cell_value & Border.NORTH:
                draw_rectangle(img_data, x, y, cell_size + wall_width,
                               wall_width, color)
            if cell_value & Border.SOUTH:
                draw_rectangle(img_data, x, y + cell_size,
                               cell_size + wall_width, wall_width, color)
            if cell_value & Border.WEST:
                draw_rectangle(img_data, x, y, wall_width,
                               cell_size + wall_width, color)
            if cell_value & Border.EAST:
                draw_rectangle(img_data, x + cell_size, y, wall_width,
                               cell_size + wall_width, color)


def render_frame(xvar: XVar, img_data: MLXImage) -> None:
    """Render the image to the window"""
    offset = img_data.cell_size // 2
    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win, img_data.img_ptr,
                                     offset, offset)
