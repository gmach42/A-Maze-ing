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
    parsing,
)
from src import events
from mlx import Mlx


def config_xvar(xvar: XVar, env_variable: EnvVariables):
    xvar.maze_width = env_variable.width
    xvar.maze_height = env_variable.height
    xvar.cell_size = env_variable.cell_size
    xvar.wall_width = env_variable.wall_width
    xvar.animation = env_variable.animation
    xvar.speed = env_variable.speed_animation


def main() -> None:
    xvar = XVar()

    # Mlx Initialisation
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

    # Window creation
    try:
        xvar.win = xvar.mlx.mlx_new_window(
            xvar.mlx_ptr, win_width, win_height, "A-Maze-ing"
        )
        if not xvar.win:
            raise Exception("Can't create main window")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate and draw maze
    generator = MazeGenerator(xvar.maze_height, xvar.maze_width)
    xvar.maze = Maze(
        xvar,
        xvar.maze_height,
        xvar.maze_width,
        generator.get_maze(),
        xvar.cell_size,
        xvar.wall_width,
        ColorManager.WALL,
    )
    if xvar.animation:
        xvar.mlx.mlx_loop_hook(
            xvar.mlx_ptr, draw_maze_walls_anim, xvar)
    else:
        draw_maze_walls(xvar)
    xvar.maze.regen()
    print(xvar.animation)

    start: tuple = env_variable.entry
    end: tuple = env_variable.exit
    solver = Solver(xvar.maze.maze_matrix, start, end)
    colors = {
        "start": ColorManager.START,
        "end": ColorManager.END,
        "path": ColorManager.PATH,
    }

    xvar.solution = SolutionPath(
        xvar=xvar,
        rows=xvar.maze_height,
        cols=xvar.maze_width,
        path_matrix=solver.a_star_algorithm(),
        wall_width=xvar.wall_width,
        colors=colors,
        start=start,
        end=end,
        cell_size=xvar.cell_size,
    )
    xvar.solution.draw_solution()
    render_frame(xvar, xvar.solution)

    # Event hooks
    xvar.mlx.mlx_key_hook(xvar.win, events.manage_key, xvar)
    xvar.mlx.mlx_hook(xvar.win, 2, 1, events.get_key_press, xvar)
    xvar.mlx.mlx_mouse_hook(xvar.win, 0, xvar)
    xvar.mlx.mlx_hook(xvar.win, 33, 0, events.manage_close, xvar)

    # Main loop
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    # Cleaning resources
    print("destroy images")
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.maze.img_ptr)
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.solution.img_ptr)
    print("destroy win(s)")
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
    print("destroy mlx")
    xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    main()
