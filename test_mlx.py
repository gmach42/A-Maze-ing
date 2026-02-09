import sys
from src.maze_generator import MazeGenerator
from mlx import Mlx
from src import Border
from src.solver import a_star_algorithm


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
        self.win = None


def draw_line(
    xvar: XVar,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: int,
    line_width: int = 5,
):
    """
    Draw a line from (x0, y0) to (x1, y1) using [Bresenham's line algorithm](\
        https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)

    Color format: 0xAARRGGBB (e.g., 0xFFFFFFFF for white, 0xFFFF0000 for red)

    More information in README.md
    """

    if line_width == 0:
        raise ValueError("Line_width cannot be null")

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    # Get direction of the line with the sign sx, sy
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    # Get the slope of the line:
    # - If dy > dx, the line will be more vertical
    # - If dx > dy, the line will be more horizontal
    err = dx - dy

    while True:
        # Draw a filled square around each point
        draw_square(xvar, x0, y0, line_width, color)

        # If the destination is reached, stop the loop
        if x0 == x1 and y0 == y1:
            break

        # Check README.md / Bresenham's algorithm
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def draw_maze_walls(
    xvar: XVar,
    maze: list[list[int]],
    cell_size: int = 50,
) -> None:
    """
    Draw walls around each cell using draw_line() and Border()
    """
    rows = len(maze)
    cols = len(maze[0])

    for row in range(rows):
        for col in range(cols):
            cell_value = maze[row][col]
            x = col * cell_size
            y = row * cell_size

            # Check each wall using bit flags (from Border class)
            if cell_value & Border.NORTH:
                draw_line(xvar, x, y, x + cell_size, y,
                          0xFFFFFFFF)

            if cell_value & Border.SOUTH:
                draw_line(xvar, x, y + cell_size, x + cell_size,
                          y + cell_size, 0xFFFFFFFF)

            if cell_value & Border.WEST:
                draw_line(xvar, x, y, x, y + cell_size,
                          0xFFFFFFFF)

            if cell_value & Border.EAST:
                draw_line(xvar, x + cell_size, y, x + cell_size,
                          y + cell_size, 0xFFFFFFFF)


def draw_square(xvar: XVar, x: int, y: int, size: int, color: int):
    for dy in range(-size, size + 1):
        for dx in range(-size, size + 1):
            xvar.mlx.mlx_pixel_put(xvar.mlx_ptr, xvar.win, x + dx, y +
                                   dy, color)


def draw_solution(xvar: XVar, solution: list[tuple], color: int, cell_size: int = 50):
    x0, y0 = solution[0]
    x1, y1 = solution[len(solution) - 1]

    draw_square(xvar, (x0 * cell_size + 25), (y0 * cell_size + 25), 15, color)
    draw_square(xvar, x1 * cell_size + 25, y1 * cell_size + 25, 15, color)

    # TODO Finish draw solution (beginning + end + path)


def manage_close_1(xvar: XVar):
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)


def manage_key(key, xvar):
    print(f"Got key {key}: ", end="")

    if key == 65307:  # 'ESC'
        xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
        xvar.mlx.mlx_release(xvar.mlx_ptr)
        sys.exit(0)


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
        xvar.win = xvar.mlx.mlx_new_window(
            xvar.mlx_ptr, 1600, 1600, "MLX main win"
        )
        if not xvar.win:
            raise Exception("Can't create main window")
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)

    generator: MazeGenerator = MazeGenerator(5, 5)
    test_maze = generator.get_maze().tolist()
    print(test_maze)
    draw_maze_walls(xvar, test_maze)
    start = (0, 0)
    end = (4, 4)
    solution = a_star_algorithm(test_maze, start, end)
    draw_solution(xvar, solution, 0xFFFF0000)

    # event hooks
    xvar.mlx.mlx_key_hook(xvar.win, manage_key, xvar)
    # xvar.mlx.mlx_hook(xvar.win, 2, 1, manage_key_press, xvar)
    xvar.mlx.mlx_mouse_hook(xvar.win, 0, xvar)
    xvar.mlx.mlx_hook(xvar.win, 33, 0, manage_close_1, xvar)

    # Main loop
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    # Cleaning resources
    print("destroy win(s)")
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
    print("destroy mlx")
    xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    main()
