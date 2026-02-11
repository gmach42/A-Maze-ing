import sys
from mlx import Mlx

from src.core.xvar import XVar
from src.core.img_data import ImgData
from src.maze.maze import Maze
from src.maze.generator import MazeGenerator
from src.solver.solver import Solver
from src.solver.path import Path
from src.rendering.renderer import setup_image_buffer, render_frame
from src.rendering.color_manager import ColorManager
from src.events.keyboard import manage_key, get_key_press
from src.events.window import manage_close


def main() -> None:
    xvar = XVar()

    try:
        xvar.mlx = Mlx()
        xvar.mlx_ptr = xvar.mlx.mlx_init()
        _, xvar.screen_w, xvar.screen_h = xvar.mlx.mlx_get_screen_size(xvar.mlx_ptr)
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)

    wall_width = 10
    if wall_width % 2:
        wall_width += 1

    try:
        cell_size = int(input("Enter the cell size: "))
        if cell_size <= 0:
            raise ValueError("Cell size must be positive")
        cols = int(input("Enter maze width: "))
        if cols <= 0:
            raise ValueError("Width must be positive")
        rows = int(input("Enter maze height: "))
        if rows <= 0:
            raise ValueError("Height must be positive")

        win_width = (cols + 1) * cell_size + wall_width
        win_height = (rows + 1) * cell_size + wall_width
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        xvar.win = xvar.mlx.mlx_new_window(xvar.mlx_ptr, win_width,
                                           win_height, "A-Maze-ing")
        if not xvar.win:
            raise Exception("Can't create main window")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    img_maze = setup_image_buffer(xvar, cols, rows, cell_size, wall_width)
    img_path = setup_image_buffer(xvar, cols, rows, cell_size, wall_width)

    generator = MazeGenerator(rows, cols)
    maze_matrix = generator.get_maze().tolist()

    xvar.maze = Maze(img_maze, rows, cols, maze_matrix, cell_size,
                     wall_width, ColorManager.WHITE)
    xvar.maze.regen_maze()

    start = (0, 0)
    end = (rows - 1, cols - 1)
    solution = Solver.a_star_algorithm(maze_matrix, start, end)

    colors = {
        "start": ColorManager.RED,
        "end": ColorManager.MAGENTA,
        "path": ColorManager.PATH,
    }
    Path.draw_solution(img_path, solution, colors, cell_size, wall_width)

    render_frame(xvar, img_maze, cell_size)
    render_frame(xvar, img_path, cell_size)

    xvar.mlx.mlx_key_hook(xvar.win, manage_key, xvar)
    xvar.mlx.mlx_hook(xvar.win, 2, 1, get_key_press, xvar)
    xvar.mlx.mlx_hook(xvar.win, 33, 0, manage_close, xvar)

    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    print("Cleaning up...")
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, img_maze.img)
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, img_path.img)
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
    xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    main()
