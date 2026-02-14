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


def config_xvar(xvar: XVar, env_variable: EnvVariables):
    xvar.animation = env_variable.animation
    xvar.speed = env_variable.speed_animation


def main() -> None:
    xvar = XVar()

    # Mlx Initialisation
    try:
        xvar.mlx = Mlx()
        xvar.mlx_ptr = xvar.mlx.mlx_init()
        _, xvar.screen_w, xvar.screen_h = xvar.mlx.mlx_get_screen_size(
            xvar.mlx_ptr)
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)

    # Get user input
    try:
        if len(sys.argv) > 2:
            raise ExecutionError("Too much arguments!")
        elif len(sys.argv) < 2:
            config_file: str = "config.txt"
        else:
            config_file = sys.argv[1]
        env_variable: EnvVariables = parsing_config(config_file)
        config_xvar(xvar, env_variable)
        win_width = (env_variable.width + 1) * env_variable.cell_size

        # Add panel's width
        panel_width: int = win_width // 3

        # Define window width and height and validate it
        win_width += panel_width
        win_height = (env_variable.height + 1) * env_variable.cell_size
        if not parsing.is_valid_window(xvar.screen_w, xvar.screen_h, win_width,
                                       win_height):
            raise ValueError("Invalid Window size")
    except ValidationError as e:
        for error in e.errors():
            print(
                f"Error in configuration file: "
                f"{error['loc'][0]} - {error['msg']}",
                file=sys.stderr,
            )
        sys.exit(1)
    except ValueError as e:
        print(
            "Please enter a valid value for the initialisation of the maze:",
            e,
            file=sys.stderr,
        )
        sys.exit(1)
    except ExecutionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Window creation
    try:
        xvar.win = xvar.mlx.mlx_new_window(xvar.mlx_ptr, win_width, win_height,
                                           "A-Maze-ing")
        if not xvar.win:
            raise Exception("Can't create main window")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Generate and draw maze
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
    # Generate solution and draw it
    try:
        xvar.solver = Solver(
            xvar.maze.maze_matrix,
            xvar.maze.entry,
            xvar.maze.exit,
            xvar.generator.forty_two_gps,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

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
        end=xvar.maze.exit,
        cell_size=xvar.maze.cell_size,
    )

    # Output maze to txt file
    output_maze(xvar.maze.maze_matrix, xvar.solution.path_matrix)

    render_init(xvar.maze)

    # Generate MazeUIManager
    xvar.manager = MazeUIManager(xvar, panel_width - 10)
    xvar.manager.draw_panel(xvar)

    if xvar.animation:
        xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, draw_maze_walls_anim, xvar)
    else:
        draw_maze_walls(xvar)
        render_frame(xvar, xvar.maze)
        xvar.solution.draw_solution()
        # render_frame(xvar, xvar.solution)

    # Starting message
    print("\nWelcome to A-Maze-ing!\n")
    print(
        f"Generating maze of size {env_variable.width}x{env_variable.height}")
    print(f"START at {env_variable.entry} and EXIT at {env_variable.exit}\n")

    # Event hooks
    xvar.mlx.mlx_key_hook(xvar.win, events.manage_key, xvar)
    # xvar.mlx.mlx_hook(xvar.win, 2, 1, events.get_key_press, xvar)
    xvar.mlx.mlx_mouse_hook(xvar.win, handle_click, xvar)
    xvar.mlx.mlx_hook(xvar.win, 33, 0, events.manage_close, xvar)

    # Main loop
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    # Cleaning resources
    print("destroy images")
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.maze.img_ptr)
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.solution.img_ptr)
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.manager.img_ptr)
    for button in xvar.manager.buttons:
        xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, button.img_ptr)
    print("destroy win(s)")
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
    print("destroy mlx")
    xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    main()
