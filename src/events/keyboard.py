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
        # TODO: change_SolutionPath_color(xvar)

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
    xvar.maze.change_color(new_color, xvar)
    render_frame(xvar, xvar.maze)


def get_key_press(key, xvar: XVar) -> int:
    """Helper to print key pressed"""
    print(f"Pressed key {key}")
