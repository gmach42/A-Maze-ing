from src.core import ImgData, XVar
from src.solver import Border


def setup_image_buffer(
    xvar: XVar, width: int, height: int, cell_size: int, wall_width: int
) -> ImgData:
    """Create an image buffer"""
    img_data = ImgData()
    img_data.width = width * cell_size + wall_width + 1
    img_data.height = height * cell_size + wall_width + 1
    img_data.img = xvar.mlx.mlx_new_image(
        xvar.mlx_ptr, img_data.width, img_data.height
    )
    res = xvar.mlx.mlx_get_data_addr(img_data.img)
    img_data.data = res[0].cast("I")
    return img_data


def draw_rectangle(
    img_data: ImgData, x: int, y: int, width: int, height: int, color: int
) -> None:
    """Draw a filled rectangle"""
    for dy in range(y, y + height):
        for dx in range(x, x + width):
            offset = dy * img_data.width + dx
            img_data.data[offset] = color


def draw_maze_walls(
    img_data: ImgData,
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
                draw_rectangle(
                    img_data, x, y, cell_size + wall_width, wall_width, color
                )
            if cell_value & Border.SOUTH:
                draw_rectangle(
                    img_data,
                    x,
                    y + cell_size,
                    cell_size + wall_width,
                    wall_width,
                    color,
                )
            if cell_value & Border.WEST:
                draw_rectangle(
                    img_data, x, y, wall_width, cell_size + wall_width, color
                )
            if cell_value & Border.EAST:
                draw_rectangle(
                    img_data,
                    x + cell_size,
                    y,
                    wall_width,
                    cell_size + wall_width,
                    color,
                )


def render_frame(xvar: XVar, img_data: ImgData, cell_size: int) -> None:
    """Render the image to the window"""
    offset = cell_size // 2
    xvar.mlx.mlx_put_image_to_window(
        xvar.mlx_ptr, xvar.win, img_data.img, offset, offset
    )
