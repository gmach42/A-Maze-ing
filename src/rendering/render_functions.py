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


def draw_maze_walls(xvar: XVar) -> None:
    """Draw walls around each cell"""

    list_ft: list = []
    for row in range(xvar.maze.rows):
        for col in range(xvar.maze.cols):
            cell_value = xvar.maze.maze_matrix[row][col]
            y = row * xvar.maze.cell_size
            x = col * xvar.maze.cell_size
            if cell_value == (Border.NORTH | Border.SOUTH | Border.EAST |
                              Border.WEST):
                list_ft.append((x, y))
            else:
                if cell_value & Border.NORTH:
                    draw_rectangle(xvar.maze, x, y,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.wall_width, xvar.maze.color)
                if cell_value & Border.SOUTH:
                    draw_rectangle(xvar.maze, x, y + xvar.maze.cell_size,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.wall_width, xvar.maze.color)
                if cell_value & Border.WEST:
                    draw_rectangle(xvar.maze, x, y, xvar.maze.wall_width,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.color)
                if cell_value & Border.EAST:
                    draw_rectangle(xvar.maze, x + xvar.maze.cell_size, y,
                                   xvar.maze.wall_width,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.color)
    for ft in list_ft:
        x, y = ft
        a: int = (xvar.maze.color >> 24) & 0xFF
        r: int = (xvar.maze.color >> 16) & 0xFF
        g: int = (xvar.maze.color >> 8) & 0xFF
        b: int = (xvar.maze.color) & 0xFF

        # We are increasing the intensity
        if (r + g + b) > 400:
            factor: float = 0.5
        else:
            factor = 1.8
        r_h = min(int(r * factor), 255)
        g_h = min(int(g * factor), 255)
        b_h = min(int(b * factor), 255)

        # If it's pure White/Green/Red or Blue we have to force a constrast
        if r_h == r and g_h == g and b_h == b:
            r_h, g_h, b_h = [int(c * 0.5) for c in (r, g, b)]

        color: int = (a << 24 | r_h << 16 | g_h << 8 | b_h)
        draw_rectangle(xvar.maze, x, y,
                       xvar.maze.cell_size + xvar.maze.wall_width,
                       xvar.maze.wall_width, color)
        draw_rectangle(xvar.maze, x, y + xvar.maze.cell_size,
                       xvar.maze.cell_size + xvar.maze.wall_width,
                       xvar.maze.wall_width, color)
        draw_rectangle(xvar.maze, x, y, xvar.maze.wall_width,
                       xvar.maze.cell_size + xvar.maze.wall_width,
                       color)
        draw_rectangle(xvar.maze, x + xvar.maze.cell_size, y,
                       xvar.maze.wall_width,
                       xvar.maze.cell_size + xvar.maze.wall_width,
                       color)


def render_frame(xvar: XVar, img_data: MLXImage) -> None:
    """Render the image to the window"""
    offset = img_data.cell_size // 2
    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win, img_data.img_ptr,
                                     offset, offset)
