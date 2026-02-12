from ..core import XVar


def manage_key(key, xvar: XVar) -> int:
    """Handle key press events"""
    print(f"Got key {key}: ", end="")

    if key == 65307:  # ESC
        print("'ESC' key pressed, exiting...")
        xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)
        return 0

    if key == 99:  # 'c'
        print("'c' key pressed, changing maze color...")
        change_maze_color(xvar)

    if key == 115:  # 's'
        print("'s' key pressed, changing solution color...")
        change_solution_color(xvar)

    if key == 114:  # 'r'
        print("'r' key pressed, regenerating maze...")
        # TODO: regenerate_maze(xvar)

    return 0


def change_maze_color(xvar: XVar) -> None:
    from ..rendering import ColorManager, render_frame
    color_index = ColorManager.COLOR_LIST.index(xvar.maze.color)
    if color_index == len(ColorManager.COLOR_LIST) - 1:
        new_color = ColorManager.COLOR_LIST[0]
    else:
        new_color = ColorManager.COLOR_LIST[color_index + 1]

    print(f"Changing to: {ColorManager.get_color_name(new_color)}")
    xvar.maze.change_color(new_color)
    render_frame(xvar, xvar.maze)


def change_solution_color(xvar: XVar) -> None:
    from ..rendering import ColorManager, render_frame
    colors_index = ColorManager.PATH_COLOR_LIST.index(
        (xvar.solution.colors["start"], xvar.solution.colors["end"],
         xvar.solution.colors["path"]))
    if colors_index == len(ColorManager.PATH_COLOR_LIST) - 1:
        new_colors = ColorManager.PATH_COLOR_LIST[0]
    else:
        new_colors = ColorManager.PATH_COLOR_LIST[colors_index + 1]
    print(
        f"Changing path color to: {ColorManager.get_color_name(new_colors[0])}"
    )
    xvar.solution.change_color({
        "start": new_colors[0],
        "end": new_colors[1],
        "path": new_colors[2],
    })
    render_frame(xvar, xvar.solution)


def get_key_press(key, xvar: XVar) -> int:
    """Helper to print key pressed"""
    print(f"Pressed key {key}")
