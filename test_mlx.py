import sys
from mlx import Mlx  # Import Mlx class
# from .solver import Border


class ImgData:
    """Structure for image data"""

    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0


class XVar:
    """Structure for main vars"""

    def __init__(self):
        self.mlx = None
        self.mlx_ptr = None
        self.screen_w = 0
        self.screen_h = 0
        self.win_1 = None


def draw_line(mlx, mlx_ptr, win, x0, y0, x1, y1, color):
    """
    Draw a line from (x0, y0) to (x1, y1) using Bresenham's algorithm
    color format: 0xAARRGGBB (e.g., 0xFFFFFFFF for white, 0xFFFF0000 for red)
    """

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        mlx.mlx_pixel_put(mlx_ptr, win, x0, y0, color)

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def draw_maze_walls(mlx, mlx_ptr, win, maze, cell_size=50):
    rows = len(maze)
    cols = len(maze[0])

    for row in range(rows):
        for col in range(cols):
            cell_value = maze[row][col]
            x = col * cell_size
            y = row * cell_size

            # Check each wall using bit flags (from Border class)
            if cell_value & 1:  # NORTH wall
                draw_line(mlx, mlx_ptr, win, x, y, x + cell_size, y,
                          0xFFFFFFFF)

            if cell_value & 4:  # SOUTH wall
                draw_line(mlx, mlx_ptr, win, x, y + cell_size,
                          x + cell_size, y + cell_size, 0xFFFFFFFF)

            if cell_value & 8:  # WEST wall
                draw_line(mlx, mlx_ptr, win, x, y, x, y + cell_size,
                          0xFFFFFFFF)

            if cell_value & 2:  # EAST wall
                draw_line(mlx, mlx_ptr, win, x + cell_size, y,
                          x + cell_size, y + cell_size, 0xFFFFFFFF)


def manage_close_1(xvar):
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)


def main():

    xvar = XVar()
    try:
        xvar.mlx = Mlx()
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)
    xvar.mlx_ptr = xvar.mlx.mlx_init()
    ret, xvar.screen_w, xvar.screen_h = xvar.mlx.mlx_get_screen_size(
        xvar.mlx_ptr
    )
    print(f"Screen size: {xvar.screen_w} x {xvar.screen_h}")

    # Windows creation
    try:
        xvar.win_1 = xvar.mlx.mlx_new_window(
            xvar.mlx_ptr, 1600, 1600, "MLX main win"
        )
        if not xvar.win_1:
            raise Exception("Can't create main window")
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)

    # xvar.img_1.img = xvar.mlx.mlx_new_image(xvar.mlx_ptr, 100, 100)
    # if not xvar.img_1.img:
    #     raise Exception("Can't create image 1")

    # xvar.img_1.width = 100
    # xvar.img_1.height = 100
    # xvar.img_1.data, xvar.img_1.bpp, xvar.img_1.sl, xvar.img_1.iformat = (
    #     xvar.mlx.mlx_get_data_addr(xvar.img_1.img)
    # )

    # for i in range(xvar.img_1.sl * 100):
    #     xvar.img_1.data[i] = 0xFF
    test_maze = [[7, 1, 11, 13], [5, 8, 5, 10], [14, 6, 8, 13], [7, 3, 2, 10]]
    # draw_line(xvar.mlx, xvar.mlx_ptr, xvar.win_1, (0, 0), (500, 500), 0xFFFFFFFF)
    draw_maze_walls(xvar.mlx, xvar.mlx_ptr, xvar.win_1, test_maze)

    # event hooks
    # xvar.mlx.mlx_key_hook(xvar.win_1, manage_key, xvar)
    # xvar.mlx.mlx_expose_hook(xvar.win_1, manage_expose, xvar)
    xvar.mlx.mlx_mouse_hook(xvar.win_1, 0, xvar)
    xvar.mlx.mlx_hook(xvar.win_1, 33, 0, manage_close_1, xvar)

    # Main loop
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    # Cleaning resources
    print("destroy win(s)")
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win_1)
    print("destroy mlx")
    xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    main()
