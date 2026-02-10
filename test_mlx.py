import sys
from src.maze_generator import MazeGenerator
from mlx import Mlx
from src import Border
from src.solver import a_star_algorithm
from typing import Any


class ImgData:
    """Structure for image data"""

    def __init__(self):
        self.img: Any = None  # mlx_new_image
        self.width: int = 0
        self.height: int = 0
        self.data: Any = None  # memoryview(int)


class XVar:
    """Structure for main vars"""

    def __init__(self):
        self.mlx: Mlx | None = None
        self.mlx_ptr: Any = None
        self.screen_w: int = 0
        self.screen_h: int = 0
        self.win: Any = None


def draw_line(
    img_data: ImgData,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: int,
    line_width: int = 5,
) -> None:
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
        draw_square(img_data, x0, y0, line_width, color)

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


def setup_image_buffer(
    xvar: XVar,
    width: int,
    height: int,
    cell_size: int
) -> ImgData:
    """
    Create an image buffer ImgData of dimension
    (`width` x `cell_size`) x (`height` x `cell_size`)
    plus 5 pixels for the line width (to avoid cutting the walls)
    """

    img_data = ImgData()
    # line_width = 5, so we need to add 2.5 to each side
    img_data.width = width * cell_size + 5
    img_data.height = height * cell_size + 5
    img_data.img = xvar.mlx.mlx_new_image(
        xvar.mlx_ptr, img_data.width, img_data.height)

    res = xvar.mlx.mlx_get_data_addr(img_data.img)
    img_data.data = res[0]

    return img_data


def put_pixel_to_image(img_data: ImgData, x: int, y: int, color: int) -> None:
    """
    Register pixel into img_data thanks to https://github.com/vgauther/mlx_img
    """

    # Separate a decimal color into 3 part rgb (255, 255, 255) + alpha
    alpha = (color >> 24) & 0xff
    red = (color >> 16) & 0xff
    green = (color >> 8) & 0xff
    blue = color & 0xff

    # Check if the pixel is in the allowed boundaries
    if 0 <= x < img_data.width and 0 <= y < img_data.height:

        # Cible le premier bit d'un pixel
        offset = y * 4 * img_data.width + x * 4
        img_data.data[offset] = blue
        img_data.data[offset + 1] = green
        img_data.data[offset + 2] = red
        img_data.data[offset + 3] = alpha


def draw_maze_walls(
    img_data: ImgData,
    maze: list[list[int]],
    cell_size: int = 50,
) -> None:
    """
    Draw walls around each cell using `draw_line()` and `Border`
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
                draw_line(img_data, x, y, x + cell_size, y,
                          0xFFFFFFFF)

            if cell_value & Border.SOUTH:
                draw_line(img_data, x, y + cell_size, x + cell_size,
                          y + cell_size, 0xFFFFFFFF)

            if cell_value & Border.WEST:
                draw_line(img_data, x, y, x, y + cell_size,
                          0xFFFFFFFF)

            if cell_value & Border.EAST:
                draw_line(img_data, x + cell_size, y, x + cell_size,
                          y + cell_size, 0xFFFFFFFF)


def draw_square(img_data: ImgData, x: int, y: int, size: int, color: int
                ) -> None:
    """Draw a filled square of size `size` centered on (`x`, `y`)"""
    for dy in range(-size, size + 1):
        for dx in range(-size, size + 1):
            put_pixel_to_image(img_data, x + dx, y + dy, color)


def draw_solution(
        img_data: ImgData, solution: list[tuple], colors: dict, cell_size: int
        ) -> None:
    """Draw the solution path on the maze using `draw_square()`"""
    x0, y0 = solution[0]
    x1, y1 = solution[len(solution) - 1]
    size_path = round(cell_size / 3)
    offset = round(cell_size / 2)

    draw_square(
        img_data, (x0 * cell_size + offset), (y0 * cell_size + offset),
        size_path, colors['start']
        )
    draw_square(
        img_data, x1 * cell_size + offset, y1 * cell_size + offset,
        size_path, colors['end']
        )
    for s in solution[1:len(solution) - 1]:
        y, x = s
        draw_square(
            img_data, x * cell_size + offset, y * cell_size + offset,
            size_path, colors['path']
            )
    # TODO Finish draw solution (beginning + end + path)


def render_frame(xvar: XVar, img_data: ImgData, cell_size: int) -> None:
    """Render the image to the window with an offset to center the maze"""
    offset: int = round(cell_size / 2)
    xvar.mlx.mlx_put_image_to_window(
        xvar.mlx_ptr, xvar.win, img_data.img, offset, offset)


def manage_close_1(xvar: XVar) -> None:
    """Handle the close event by exiting the MLX loop"""
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)


def manage_key(key, xvar) -> None:
    """Handle key press events"""
    print(f"Got key {key}: ", end="")

    if key == 65307:  # 'ESC'
        print("'ESC' key pressed, exciting...")
        xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)
        return 0

    if key == 99:  # 'c'
        print("'c' key pressed, changing color of the maze...")
        # TODO change color of the maze

    if key == 52:  # '4'
        print("'4' key pressed, changing 42 symbol color...")
        # TODO change color of 42 symbol

    if key == 115:  # 's'
        print("'s' key pressed, changing color of the solution path...")
        # TODO change color of the solution path

    if key == 114:  # 'r'
        print("'r' key pressed, regenerating maze...")
        # TODO regenerate maze

    return 0


def get_key_press(key, xvar):
    """little helper function to print the key pressed"""
    print(f"Pressed key {key}")


def main() -> None:

    # Mlx Initialisation
    xvar = XVar()
    try:
        xvar.mlx = Mlx()
        xvar.mlx_ptr = xvar.mlx.mlx_init()
        _, xvar.screen_w, xvar.screen_h = xvar.mlx.mlx_get_screen_size(
            xvar.mlx_ptr)
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)

    # Get user input for maze dimensions and cell size
    try:
        cell_size: int = int(input("Enter the cell size: "))
        if cell_size <= 0:
            raise ValueError
        maze_width: int = int(input("Enter the desired width of your maze: "))
        if maze_width <= 0:
            raise ValueError
        maze_height: int = int(input("Enter the desired height of your maze: "))
        if maze_height <= 0:
            raise ValueError
        win_width = (maze_width + 1) * cell_size
        win_height = (maze_height + 1) * cell_size
    except ValueError:
        print(
            "Please enter a valid value for the initialisation of the maze",
            file=sys.stderr)
        sys.exit(1)

    # Windows creation
    try:
        xvar.win = xvar.mlx.mlx_new_window(
            xvar.mlx_ptr, win_width, win_height, "A-Maze-ing")
        if not xvar.win:
            raise Exception("Can't create main window")
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)

    # Create new image buffer
    img_data = setup_image_buffer(xvar, maze_width, maze_height, cell_size)
    if not img_data:
        raise Exception("no image created")

    # generate and draw maze
    generator: MazeGenerator = MazeGenerator(maze_height, maze_width)
    test_maze = generator.get_maze().tolist()
    print(test_maze)
    draw_maze_walls(img_data, test_maze)

    start = (0, 0)
    print(f'{start=}')
    end = (14, 14)
    print(f'{end=}')
    solution = a_star_algorithm(test_maze, start, end)
    colors: dict = {
        'start': 0xFFFF0000,    # Red
        'end': 0xFFFF00FF,      # Magenta
        'path': 0xFF7B68EE      # Medium slate blue
    }
    draw_solution(img_data, solution, colors, cell_size)

    # Print the image once it is fully implemented ->
    # Only 1 call instead of thousands with mlx_pixel_pit()
    render_frame(xvar, img_data, cell_size)

    # Event hooks
    xvar.mlx.mlx_key_hook(xvar.win, manage_key, xvar)
    xvar.mlx.mlx_hook(xvar.win, 2, 1, get_key_press, xvar)
    xvar.mlx.mlx_mouse_hook(xvar.win, 0, xvar)
    xvar.mlx.mlx_hook(xvar.win, 33, 0, manage_close_1, xvar)

    # Main loop
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    # Cleaning resources
    print("destroy image (to prevent leaks kek)")
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, img_data.img)
    print("destroy win(s)")
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
    print("destroy mlx")
    xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    main()
