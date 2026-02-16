from ..core import XVar
from ..rendering.render_functions import draw_42, display_path

HELP_MESSAGE = """
╔══════════════════════════════════════════════════════╗
║           A-MAZE-ING - KEYBINDS HELP                 ║
╠══════════════════════════════════════════════════════╣
║  ESC   │ Exit application                            ║
║  a     │ Change Maze generation algorithm            ║
║  c     │ Cycle maze wall colors                      ║
║  d     │ Display/Hide solution path                  ║
║  s     │ Cycle solution path colors                  ║
║  g     │ Toggle 42 animation                         ║
║  r     │ Regenerate new maze                         ║
║  h     │ Show this help message                      ║
╚══════════════════════════════════════════════════════╝
"""


def manage_key(key: int, xvar: XVar) -> int:
    from ..rendering import MazeUIManager
    """Handle key press events"""

    # Uncomment this if you want to get the id of the key pressed:
    # print(f"Got key {key}: ")

    if key == 65307:  # ESC
        print("\n'ESC' key pressed, exiting...")
        xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)

    if key == 99:  # 'c'
        print("\n'c' key pressed, changing maze color...")
        change_maze_color(xvar)

    if key == 115:  # 's'
        print("\n's' key pressed, changing solution color...")
        change_solution_color(xvar)

    if key == 103:  # 'g'
        print("\n'g' key pressed, changing 42's color...")
        change_42_color(xvar)

    if key == 114:  # 'r'
        print("\n'r' key pressed, regenerating maze...")
        MazeUIManager.regenerate(xvar)

    if key == 100:  # 'd'
        print("\n'd' key pressed, displaying/hiding path...")
        display_path(xvar)

    if key == 104:  # 'h'
        print("\n'h' key pressed, showing help message...")
        print(HELP_MESSAGE)

    if key == 97:  # 'a'
        print("\n'a' key pressed, changing maze algortihm...")
        change_algo(xvar)
        MazeUIManager.regenerate(xvar)

    return 0


def change_maze_color(xvar: XVar) -> None:
    """Change maze wall color and redraw the maze."""
    if xvar.mlx._python_ref_std.get("loop_f"):
        print("Wait until the animation ends")
    else:
        from ..rendering import ColorManager, render_frame
        color_index = ColorManager.COLOR_LIST.index(xvar.maze.color)
        if color_index == len(ColorManager.COLOR_LIST) - 1:
            new_color = ColorManager.COLOR_LIST[0]
        else:
            new_color = ColorManager.COLOR_LIST[color_index + 1]

        print(f"Changing to: {ColorManager.get_color_name(new_color)}")
        xvar.maze.change_color(new_color, xvar)
        render_frame(xvar, xvar.maze)


def change_42_color(xvar: XVar) -> None:
    """Change 42's color and redraw it."""
    if len(xvar.generator.forty_two_gps) > 0:
        if xvar.animation:
            if not xvar.mlx._python_ref_std.get("loop_f"):
                xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, draw_42, xvar)
            else:
                if xvar.row == xvar.maze.rows and (
                    (xvar.solution.step == len(xvar.solution.path_matrix)
                     and xvar.solution.display) or
                   (xvar.solution.step == 0 and not xvar.solution.display)):
                    xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, None, None)
                else:
                    print("Wait until the animation ends")
        else:
            draw_42(xvar)
    else:
        print("No 42 in this maze. Don't waste your time clicking")


def change_algo(xvar: XVar) -> None:
    """Change maze generation algorithm"""
    if xvar.generator.algo == 1:
        xvar.generator.algo = 2
    elif xvar.generator.algo == 2:
        xvar.generator.algo = 1
    print("The algorithm has been changed.")


def change_solution_color(xvar: XVar) -> None:
    """Change solution path color and redraw it."""
    if xvar.mlx._python_ref_std.get("loop_f"):
        print("Wait until the animation ends")
    else:
        from ..rendering import ColorManager, render_frame
        colors_index = ColorManager.PATH_COLOR_LIST.index(
            (xvar.solution.colors["start"], xvar.solution.colors["end"],
             xvar.solution.colors["path"]))
        if colors_index == len(ColorManager.PATH_COLOR_LIST) - 1:
            new_colors = ColorManager.PATH_COLOR_LIST[0]
        else:
            new_colors = ColorManager.PATH_COLOR_LIST[colors_index + 1]
        print("Changing path color to:"
              f" {ColorManager.get_color_name(new_colors[2])}")
        xvar.solution.change_color(
            {
                "start": new_colors[0],
                "end": new_colors[1],
                "path": new_colors[2],
            }, xvar)
        render_frame(xvar, xvar.solution)
        xvar.solution.display = True
