import sys
from src.maze_generator import MazeGenerator
from mlx import Mlx
from src import Border
from src.solver import a_star_algorithm
import src.solver as solver
from typing import Any
from src.color_manager import ColorManager


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


def setup_image_buffer(
    xvar: XVar,
    width: int,
    height: int,
    cell_size: int,
    line_width: int,
) -> ImgData:
    """
    Create an image buffer ImgData of dimension
    (`width` x `cell_size`) x (`height` x `cell_size`)
    plus 5 pixels for the line width (to avoid cutting the walls)
    """

    img_data = ImgData()

    img_data.width = width * cell_size + line_width + 1
    img_data.height = height * cell_size + line_width + 1
    print(img_data.height, img_data.width)
    img_data.img = xvar.mlx.mlx_new_image(
        xvar.mlx_ptr, img_data.width, img_data.height)

    res = xvar.mlx.mlx_get_data_addr(img_data.img)
    img_data.data = res[0].cast('I')

    return img_data


def draw_maze_walls(
    img_data: ImgData,
    maze: list[list[int]],
    cell_size: int,
    line_width: int,
    line_color: int,
) -> None:
    """
    Draw walls around each cell using `draw_rectangle` and `Border`
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
                draw_rectangle(img_data, x, y, cell_size + line_width, line_width, line_color)

            if cell_value & Border.SOUTH:
                draw_rectangle(img_data, x, y + cell_size, cell_size + line_width, line_width, line_color)

            if cell_value & Border.WEST:
                draw_rectangle(img_data, x, y, line_width, cell_size + line_width, line_color)

            if cell_value & Border.EAST:
                draw_rectangle(img_data, x + cell_size, y, line_width, cell_size + line_width, line_color)


def draw_rectangle(img_data: ImgData, x: int, y: int, width: int, height: int, color: int
                   ) -> None:
    """Draw a filled square of size `size` centered on (`x`, `y`)"""
    for dy in range(y, y + height):
        for dx in range(x, x + width):
            offset = dy * img_data.width + dx
            img_data.data[offset] = color


def draw_solution(
        img_data: ImgData, solution: list[tuple[int, int]], colors: dict[str, int], cell_size: int, line_width: int
        ) -> None:
    """Draw the solution path on the maze using `draw_rectangle()`"""
    y_start, x_start = solution[0]
    y_end, x_end = solution[-1]
    size_path = cell_size - line_width
    offset = line_width

    # Draw start
    draw_rectangle(img_data, x_start * cell_size + offset, y_start * cell_size + offset, size_path, size_path, colors['start'])

    # Draw end
    draw_rectangle(img_data, x_end * cell_size + offset, y_end * cell_size + offset, size_path, size_path, colors['end'])

    # Draw path
    for s in solution[1:len(solution) - 1]:
        y, x = s
        draw_rectangle(img_data, x * cell_size + offset, y * cell_size + offset, size_path, size_path, colors['path'])


def render_frame(xvar: XVar, img_data: ImgData, cell_size: int) -> None:
    """Render the image to the window with an offset to center the maze"""
    offset: int = cell_size // 2
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

    # if line_width not pair: line_width++
    line_width = 10
    if line_width % 2:
        line_width += 1

    # Get user input for maze dimensions and cell size
    try:
        cell_size = int(input("Enter the cell size: "))
        if cell_size <= 0:
            raise ValueError
        # line_width = int(input("Enter the line width: "))
        # if line_width <= 0:
        #     raise ValueError
        maze_width = int(input("Enter the desired width of your maze: "))
        if maze_width <= 0:
            raise ValueError
        maze_height = int(input("Enter the desired height of your maze: "))
        if maze_height <= 0:
            raise ValueError
        win_width = (maze_width + 1) * cell_size + line_width
        win_height = (maze_height + 1) * cell_size + line_width
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
    img_data = setup_image_buffer(xvar, maze_width, maze_height, cell_size, line_width)
    if not img_data:
        raise Exception("no image created")

    # Generate and draw maze
    generator: MazeGenerator = MazeGenerator(maze_height, maze_width)
    test_maze = generator.get_maze()
    print(test_maze)
    draw_maze_walls(img_data, test_maze, cell_size, line_width, ColorManager.WHITE)

    # Define start and end
    start = (0, 0)
    print(f'{start=}')
    end = (14, 14)
    print(f'{end=}')

    # Get the solution path with A* algorithm and draw it on the maze
    solution = a_star_algorithm(test_maze, start, end)
    print(f'Solution:\n{solver.cardinal_direction(solution)}')
    colors: dict = {
        'start': ColorManager.RED,
        'end': ColorManager.MAGENTA,
        'path': ColorManager.PATH
    }
    draw_solution(img_data, solution, colors, cell_size, line_width)

    # Print the image once it is fully implemented ->
    # Only 1 call instead of thousands with mlx_pixel_pit()
    render_frame(xvar, img_data, cell_size)

    # Event hooks
    xvar.mlx.mlx_key_hook(xvar.win, manage_key, xvar)
    xvar.mlx.mlx_hook(xvar.win, 2, 1, get_key_press, xvar)
    xvar.mlx.mlx_mouse_hook(xvar.win, 0, xvar)
    xvar.mlx.mlx_hook(xvar.win, 33, 0, manage_close_1, xvar)

    # Main loop
    # xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, render_function, )
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    # Cleaning resources
    print("destroy image")
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, img_data.img)
    print("destroy win(s)")
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
    print("destroy mlx")
    xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    main()
