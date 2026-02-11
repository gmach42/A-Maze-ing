import sys
import array
from src.maze_generator import MazeGenerator
from mlx import Mlx
from src import Border
from src import parsing, EnvVariables
from src.solver import a_star_algorithm
import src.solver as solver
from typing import Any
from src.color_manager import ColorManager
from src import MazeManager


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
        self.img: ImgData = None
        self.cell_size: int = 50
        self.maze: list = []
        self.col: int = 0
        self.row: int = 0
        self.maze_width: int = 0
        self.maze_height: int = 0

    def set_img(self, img: ImgData):
        self.img = img


def draw_vertical_line(
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
    xvar: XVar
) -> ImgData:
    """
    Create an image buffer ImgData of dimension
    (`width` x `cell_size`) x (`height` x `cell_size`)
    plus 5 pixels for the line width (to avoid cutting the walls)
    """

    img_data = ImgData()
    # line_width = 5, so we need to add 2.5 to each side
    img_data.width = xvar.maze_width * xvar.cell_size + 5
    img_data.height = xvar.maze_height * xvar.cell_size + 5
    img_data.img = xvar.mlx.mlx_new_image(
        xvar.mlx_ptr, img_data.width, img_data.height)

    res = xvar.mlx.mlx_get_data_addr(img_data.img)
    img_data.data = res[0].cast('I')

    return img_data


def put_line_to_image(img_data: ImgData, x: int, y: int, size: int,
                      color: int) -> None:
    """
    Register pixel into img_data thanks to https://github.com/vgauther/mlx_img
    """
    for dy in range(-5, 5 + 1):
        target_y: int = y + dy

        # Check if the pixel is in the allowed boundaries
        if 0 <= x < img_data.width and 0 <= target_y < img_data.height:

            # Cible le premier bit d'un pixel
            start = (target_y * img_data.width) + x
            end = (target_y * img_data.width) + (x + size)
            img_data.data[start:end] = array.array('I',
                                                   [color] * (end - start))


def put_pixel_to_image(img_data: ImgData, x: int, y: int, color: int) -> None:
    """
    Register pixel into img_data thanks to https://github.com/vgauther/mlx_img
    """

    # Separate a decimal color into 3 part rgb (255, 255, 255) + alpha
    # alpha = (color >> 24) & 0xff
    # red = (color >> 16) & 0xff
    # green = (color >> 8) & 0xff
    # blue = color & 0xff

    # Check if the pixel is in the allowed boundaries
    if 0 <= x < img_data.width and 0 <= y < img_data.height:

        # Cible le premier bit d'un pixel
        offset = y * img_data.width + x
        img_data.data[offset] = color
        # img_data.data[offset + 1] = green
        # img_data.data[offset + 2] = red
        # img_data.data[offset + 3] = alpha


def draw_maze_walls(
    xvar: XVar
) -> None:
    """
    Draw walls around each cell using `draw_line()` and `Border`
    """

    if (0 <= xvar.row < xvar.maze_height) and\
       (0 <= xvar.col < xvar.maze_width):
        try:
            cell_value = xvar.maze[xvar.row][xvar.col]
            x = xvar.col * xvar.cell_size
            y = xvar.row * xvar.cell_size

            # Check each wall using bit flags (from Border class)
            if cell_value & Border.NORTH:
                put_line_to_image(xvar.img, x, y, xvar.cell_size, 0xFFFFFFFF)
            if cell_value & Border.SOUTH:
                put_line_to_image(xvar.img, x, y + xvar.cell_size,
                                  xvar.cell_size, 0xFFFFFFFF)
            if cell_value & Border.WEST:
                draw_vertical_line(xvar.img, x, y, x, y + xvar.cell_size,
                                   0xFFFFFFFF)
            if cell_value & Border.EAST:
                draw_vertical_line(xvar.img, x + xvar.cell_size, y, x +
                                   xvar.cell_size, y + xvar.cell_size,
                                   0xFFFFFFFF)
            render_frame(xvar)
            xvar.col += 1
            if xvar.col >= xvar.maze_width:
                xvar.col = 0
                xvar.row += 1
        except IndexError:
            print(f"{xvar.col=} et {xvar.row=}")


def draw_square(img_data: ImgData, x: int, y: int, size: int, color: int
                ) -> None:
    """Draw a filled square of size `size` centered on (`x`, `y`)"""
    for dy in range(-size, size + 1):
        for dx in range(-size, size + 1):
            put_pixel_to_image(img_data, x + dx, y + dy, color)


def draw_solution(
        xvar: XVar, solution: list[tuple], colors: dict) -> None:
    """Draw the solution path on the maze using `draw_square()`"""
    y0, x0 = solution[0]
    y1, x1 = solution[-1]
    size_path = round(xvar.cell_size / 3)
    offset = round(xvar.cell_size / 2)

    draw_square(
        xvar.img, (x0 * xvar.cell_size + offset),
        (y0 * xvar.cell_size + offset), size_path, colors['start']
        )
    draw_square(
        xvar.img, x1 * xvar.cell_size + offset, y1 * xvar.cell_size + offset,
        size_path, colors['end']
        )
    for s in solution[1:len(solution) - 1]:
        y, x = s
        draw_square(
            xvar.img, x * xvar.cell_size + offset, y * xvar.cell_size + offset,
            size_path, colors['path']
            )
    # TODO Finish draw solution (beginning + end + path)


def render_frame(xvar: XVar) -> None:
    """Render the image to the window with an offset to center the maze"""
    offset: int = round(xvar.cell_size / 2)
    xvar.mlx.mlx_put_image_to_window(
        xvar.mlx_ptr, xvar.win, xvar.img.img, offset, offset)


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
        env_variable: EnvVariables = parsing('config.txt')
        xvar.maze_width = env_variable.width
        xvar.maze_height = env_variable.height
        win_width = (xvar.maze_width + 1) * xvar.cell_size
        win_height = (xvar.maze_height + 1) * xvar.cell_size
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
    xvar.set_img(setup_image_buffer(xvar))
    if not xvar.img:
        raise Exception("no image created")

    # Generate and draw maze
    generator: MazeGenerator = MazeGenerator(xvar.maze_height, xvar.maze_width)
    xvar.maze = generator.get_maze()
    xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, draw_maze_walls, xvar)

    # TODO Get user input for start and end points, or generate them randomly

    # Get the solution path with A* algorithm and draw it on the maze
    start: tuple = env_variable.entry
    end: tuple = env_variable.exit
    solution = a_star_algorithm(xvar.maze, start, end)
    # print(f'Solution:\n{solver.cardinal_direction(solution)}')
    colors: dict = {
        'start': ColorManager.RED,
        'end': ColorManager.MAGENTA,
        'path': ColorManager.PATH
    }
    draw_solution(xvar, solution, colors)

    # Print the image once it is fully implemented ->
    # Only 1 call instead of thousands with mlx_pixel_pit()
    render_frame(xvar)

    # Event hooks
    xvar.mlx.mlx_key_hook(xvar.win, manage_key, xvar)
    xvar.mlx.mlx_hook(xvar.win, 2, 1, get_key_press, xvar)
    xvar.mlx.mlx_mouse_hook(xvar.win, 0, xvar)
    xvar.mlx.mlx_hook(xvar.win, 33, 0, manage_close_1, xvar)

    # Main loop
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    # Cleaning resources
    print("destroy image")
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.img.img)
    print("destroy win(s)")
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
    print("destroy mlx")
    xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    main()
