import sys
from src import (
    ColorManager,
    Maze,
    SolutionPath,
    draw_maze_walls_anim,
    draw_maze_walls,
    render_frame,
    MazeGenerator,
    Solver,
    XVar,
    EnvVariables,
    parsing_config,
    handle_click,
    ExecutionError,
    MazeUIManager,
    output_maze,
    render_init,
)
from src import events, parsing
from mlx import Mlx
from pydantic import ValidationError
from src.parsing.constants import MIN_COL_42, PANEL_WIDTH, MIN_ROW_42


def config_xvar(xvar: XVar, env_variable: EnvVariables) -> None:
    xvar.animation = env_variable.animation
    xvar.speed = env_variable.speed_animation


def initialize_mlx() -> tuple[Mlx, any, int, int]:
    """Initialize MLX and get screen size."""
    try:
        mlx = Mlx()
        mlx_ptr = mlx.mlx_init()
        _, screen_w, screen_h = mlx.mlx_get_screen_size(mlx_ptr)
        return mlx, mlx_ptr, screen_w, screen_h
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)


def parse_arguments_and_config() -> tuple[EnvVariables, int, int]:
    """Parse command line arguments and configuration file."""
    if len(sys.argv) > 2:
        raise ExecutionError("Too much arguments!")

    config_file = sys.argv[1] if len(sys.argv) == 2 else "config.txt"
    env_variable = parsing_config(config_file)

    win_width = (env_variable.width + 1) * env_variable.cell_size
    win_height = (env_variable.height +
                  1) * env_variable.cell_size + env_variable.wall_width

    return env_variable, win_width, win_height


def create_window(xvar: XVar, width: int, height: int) -> any:
    """Create MLX window."""
    win = xvar.mlx.mlx_new_window(xvar.mlx_ptr, width, height, "A-Maze-ing")
    if not win:
        raise Exception("Can't create main window")
    return win


def setup_maze_and_solution(xvar: XVar, env_variable: EnvVariables) -> None:
    """Initialize maze generator, maze, solver and solution."""
    xvar.generator = MazeGenerator(env_variable.height, env_variable.width,
                                   env_variable.perfect, env_variable.seed)

    xvar.maze = Maze(
        xvar,
        env_variable.entry,
        env_variable.exit,
        env_variable.height,
        env_variable.width,
        xvar.generator.get_maze(),
        env_variable.cell_size,
        env_variable.wall_width,
        ColorManager.WALL,
    )

    xvar.solver = Solver(
        xvar.maze.maze_matrix,
        xvar.maze.entry,
        xvar.maze.exit,
        xvar.generator.forty_two_gps,
    )

    xvar.solution = SolutionPath(
        xvar=xvar,
        rows=xvar.maze.rows,
        cols=xvar.maze.cols,
        path_matrix=xvar.solver.a_star_algorithm(),
        wall_width=xvar.maze.wall_width,
        colors={
            "start": ColorManager.START,
            "end": ColorManager.END,
            "path": ColorManager.PATH,
        },
        start=xvar.maze.entry,
        end=env_variable.exit,
        cell_size=xvar.maze.cell_size,
    )


def cleanup_resources(xvar: XVar) -> None:
    """Clean up MLX resources."""
    print("\nDestroying images")
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.maze.img_ptr)
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.solution.img_ptr)
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.manager.img_ptr)
    for button in xvar.manager.buttons:
        xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, button.img_ptr)

    print("Destroying window")
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
    print("Destroying mlx")
    xvar.mlx.mlx_release(xvar.mlx_ptr)


def main() -> None:
    """
    Main entry point of the A-Maze-ing application.

    Orchestrates the program execution lifecycle:
    1. Initializes MLX and parses configuration/arguments.
    2. Creates the window and generates the maze/solution.
    3. Sets up the UI, event hooks, and rendering loop.
    4. Handles resource cleanup upon exit.
    """

    print("\nWelcome to A-Maze-ing!\n")

    xvar = XVar()

    # Initialize MLX
    xvar.mlx, xvar.mlx_ptr, xvar.screen_w, xvar.screen_h = initialize_mlx()

    # Parse configuration
    try:
        # Parse arguments from config file and calculate window size
        env_variable, win_width, win_height = parse_arguments_and_config()
        config_xvar(xvar, env_variable)

        # Add panel width to window width
        panel_width = PANEL_WIDTH
        win_width += panel_width + env_variable.cell_size

        # Validate window size
        if not parsing.is_valid_window(xvar.screen_w, xvar.screen_h, win_width,
                                       win_height):
            raise ValueError("Invalid Window size")

        # In case maze is too small to contain 42, print a warning and
        # do not generate 42 in the maze (list of 42 coordinates will be empty)
        if env_variable.width < MIN_COL_42 or env_variable.height < MIN_ROW_42:
            print('=' * 40)
            print("Little Maze setting: NO 42 in the maze!")
            print('=' * 40 + '\n')

    except (ValidationError, ValueError, ExecutionError,
            FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Create window
    try:
        xvar.win = create_window(xvar, win_width, win_height)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Setup maze and solution
    try:
        setup_maze_and_solution(xvar, env_variable)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Output and UI
    output_maze(xvar.maze.maze_matrix, xvar.solution.path_matrix)
    xvar.manager = MazeUIManager(xvar, panel_width)
    xvar.manager.draw_panel(xvar)

    # Initialize rendering to avoid glitches on first frame
    render_init(xvar.maze)
    render_init(xvar.solution)

    # Animated drawing of maze walls or static rendering
    if xvar.animation:
        xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, draw_maze_walls_anim, xvar)
    else:
        draw_maze_walls(xvar)
        render_frame(xvar, xvar.maze)
        xvar.solution.draw_solution(xvar)

    # Display maze info
    print(
        f"\nGenerating maze of size {env_variable.width}x{env_variable.height}"
    )
    print(f"START at {env_variable.entry} and EXIT at {env_variable.exit}\n")

    # Setup event hooks
    xvar.mlx.mlx_key_hook(xvar.win, events.manage_key, xvar)
    xvar.mlx.mlx_mouse_hook(xvar.win, handle_click, xvar)
    xvar.mlx.mlx_hook(xvar.win, 33, 0, events.manage_close, xvar)

    # Main loop
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    # Cleanup
    cleanup_resources(xvar)


if __name__ == "__main__":
    main()
