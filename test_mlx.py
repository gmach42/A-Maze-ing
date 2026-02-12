import sys
from src.maze_algorithm.maze_generator import MazeGenerator
from mlx import Mlx
from src import Border
from src import parsing, EnvVariables
from src.maze_algorithm.solver_algorithm import a_star_algorithm
from typing import Any
from src.rendering.color_manager import ColorManager

# TODO gestion erreur parsing et autre
# TODO merge correctement avec version gildas
# TODO animation chemin


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
        self.wall_width: int = 0
        self.line_color: ColorManager = ColorManager.WHITE
        self.animation: bool = False
        self.speed: str = "medium"
        self.solution: list = []

    def set_img(self, img: ImgData):
        self.img = img


def setup_image_buffer(xvar: XVar) -> ImgData:
    """
    Create an image buffer ImgData of dimension
    (`width` x `cell_size`) x (`height` x `cell_size`)
    plus 5 pixels for the line width (to avoid cutting the walls)
    """

    img_data = ImgData()

    img_data.width = xvar.maze_width * xvar.cell_size + xvar.wall_width + 1
    img_data.height = xvar.maze_height * xvar.cell_size + xvar.wall_width + 1
    img_data.img = xvar.mlx.mlx_new_image(
        xvar.mlx_ptr, img_data.width, img_data.height
    )

    res = xvar.mlx.mlx_get_data_addr(img_data.img)
    img_data.data = res[0].cast("I")

    return img_data


def draw_maze_walls(xvar: XVar) -> None:
    """
    Draw walls around each cell using `draw_rectangle` and `Border`
    """
    rows = len(xvar.maze)
    cols = len(xvar.maze[0])

    for row in range(rows):
        for col in range(cols):
            cell_value = xvar.maze[row][col]
            x = col * xvar.cell_size
            y = row * xvar.cell_size

            # Check each wall using bit flags (from Border class)
            if cell_value & Border.NORTH:
                draw_rectangle(
                    xvar.img,
                    x,
                    y,
                    xvar.cell_size + xvar.wall_width,
                    xvar.wall_width,
                    xvar.line_color,
                )

            if cell_value & Border.SOUTH:
                draw_rectangle(
                    xvar.img,
                    x,
                    y + xvar.cell_size,
                    xvar.cell_size + xvar.wall_width,
                    xvar.wall_width,
                    xvar.line_color,
                )

            if cell_value & Border.WEST:
                draw_rectangle(
                    xvar.img,
                    x,
                    y,
                    xvar.wall_width,
                    xvar.cell_size + xvar.wall_width,
                    xvar.line_color,
                )

            if cell_value & Border.EAST:
                draw_rectangle(
                    xvar.img,
                    x + xvar.cell_size,
                    y,
                    xvar.wall_width,
                    xvar.cell_size + xvar.wall_width,
                    xvar.line_color,
                )


def draw_maze_walls_anim(xvar: XVar) -> None:
    """
    Draw walls around each cell using `draw_rectangle` and `Border`
    """
    match xvar.speed:
        case "slow":
            limit: int = 1
        case "medium":
            limit: int = 5
        case "fast":
            limit: int = 10

    for _ in range(limit):
        if (0 <= xvar.row < xvar.maze_height) and (
            0 <= xvar.col < xvar.maze_width
        ):
            try:
                cell_value = xvar.maze[xvar.row][xvar.col]
                x = xvar.col * xvar.cell_size
                y = xvar.row * xvar.cell_size

                # Check each wall using bit flags (from Border class)
                if cell_value & Border.NORTH:
                    draw_rectangle(
                        xvar.img,
                        x,
                        y,
                        xvar.cell_size + xvar.wall_width,
                        xvar.wall_width,
                        xvar.line_color,
                    )

                if cell_value & Border.SOUTH:
                    draw_rectangle(
                        xvar.img,
                        x,
                        y + xvar.cell_size,
                        xvar.cell_size + xvar.wall_width,
                        xvar.wall_width,
                        xvar.line_color,
                    )

                if cell_value & Border.WEST:
                    draw_rectangle(
                        xvar.img,
                        x,
                        y,
                        xvar.wall_width,
                        xvar.cell_size + xvar.wall_width,
                        xvar.line_color,
                    )

                if cell_value & Border.EAST:
                    draw_rectangle(
                        xvar.img,
                        x + xvar.cell_size,
                        y,
                        xvar.wall_width,
                        xvar.cell_size + xvar.wall_width,
                        xvar.line_color,
                    )
                render_frame(xvar)
                xvar.col += 1
                if xvar.col >= xvar.maze_width:
                    xvar.col = 0
                    xvar.row += 1
            except IndexError:
                print(f"{xvar.col=} et {xvar.row=}")


def draw_rectangle(
    img_data: ImgData, x: int, y: int, width: int, height: int, color: int
) -> None:
    """Draw a filled square of size `size` centered on (`x`, `y`)"""
    for dy in range(y, y + height):
        for dx in range(x, x + width):
            offset = dy * img_data.width + dx
            img_data.data[offset] = color


def draw_solution(
    xvar: XVar, solution: list[tuple[int, int]], colors: dict[str, int]
) -> None:
    """Draw the solution path on the maze using `draw_rectangle()`"""
    y_start, x_start = solution[0]
    y_end, x_end = solution[-1]
    size_path = xvar.cell_size - xvar.wall_width
    offset = xvar.wall_width

    # Draw start
    draw_rectangle(
        xvar.img,
        x_start * xvar.cell_size + offset,
        y_start * xvar.cell_size + offset,
        size_path,
        size_path,
        colors["start"],
    )

    # Draw end
    draw_rectangle(
        xvar.img,
        x_end * xvar.cell_size + offset,
        y_end * xvar.cell_size + offset,
        size_path,
        size_path,
        colors["end"],
    )

    # Draw path
    for s in solution[1: len(solution) - 1]:
        y, x = s
        draw_rectangle(
            xvar.img,
            x * xvar.cell_size + offset,
            y * xvar.cell_size + offset,
            size_path,
            size_path,
            colors["path"],
        )


def render_frame(xvar: XVar) -> None:
    """Render the image to the window with an offset to center the maze"""
    offset: int = xvar.cell_size // 2
    xvar.mlx.mlx_put_image_to_window(
        xvar.mlx_ptr, xvar.win, xvar.img.img, offset, offset
    )


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
        print(
            "'s' key pressed, changing color of the solution SolutionPath..."
        )
        # TODO change color of the solution SolutionPath

    if key == 114:  # 'r'
        print("'r' key pressed, regenerating maze...")
        # TODO regenerate maze

    return 0


def get_key_press(key, xvar):
    """little helper function to print the key pressed"""
    print(f"Pressed key {key}")


def config_xvar(xvar: XVar, env_variable: EnvVariables):
    xvar.maze_width = env_variable.width
    xvar.maze_height = env_variable.height
    xvar.cell_size = env_variable.cell_size
    xvar.wall_width = env_variable.wall_width
    xvar.animation = env_variable.animation
    xvar.speed = env_variable.speed_animation


def main() -> None:

    # Mlx Initialisation
    xvar = XVar()
    try:
        xvar.mlx = Mlx()
        xvar.mlx_ptr = xvar.mlx.mlx_init()
        _, xvar.screen_w, xvar.screen_h = xvar.mlx.mlx_get_screen_size(
            xvar.mlx_ptr
        )
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)

    # Get user input for maze dimensions and cell size
    try:
        env_variable: EnvVariables = parsing("config.txt")
        config_xvar(xvar, env_variable)
        win_width = (xvar.maze_width + 1) * xvar.cell_size
        win_height = (xvar.maze_height + 1) * xvar.cell_size
    except ValueError:
        print(
            "Please enter a valid value for the initialisation of the maze",
            file=sys.stderr,
        )
        sys.exit(1)

    # Windows creation
    try:
        xvar.win = xvar.mlx.mlx_new_window(
            xvar.mlx_ptr, win_width, win_height, "A-Maze-ing"
        )
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
    if xvar.animation:
        xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, draw_maze_walls_anim, xvar)
    else:
        draw_maze_walls(xvar)

    # Get the solution path with A* algorithm and draw it on the maze
    start: tuple = env_variable.entry
    end: tuple = env_variable.exit
    solution = a_star_algorithm(xvar.maze, start, end)
    # print(f'Solution:\n{solver.cardinal_direction(solution)}')
    colors: dict = {
        "start": ColorManager.RED,
        "end": ColorManager.MAGENTA,
        "path": ColorManager.PATH,
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
    # xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, render_function, )
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
