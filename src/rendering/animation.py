from ..core import XVar
from ..maze_algorithm import Border
from .render_functions import draw_rectangle, render_frame, draw_42


def draw_maze_walls_anim(xvar: XVar) -> None:
    """
    Main function to draw the **maze walls** with **animation**.

    It iterates through the maze matrix and draws each cell's walls based on
    the presence of walls using bit flags. The animation speed is controlled
    by the `speed` attribute of `XVar`, which determines how many cells are
    drawn per frame. Once all cells are drawn, it checks if the solution path
    should be displayed and sets up the appropriate rendering hooks for the
    solution animation or static display.

    Raises:
        IndexError: If the current row or column exceeds the maze dimensions.
    """
    match xvar.speed:
        case "slow":
            limit: int = 1
        case "medium":
            limit = 5
        case "fast":
            limit = 10

    for _ in range(limit):
        if (0 <= xvar.row < xvar.maze.rows) and (0 <= xvar.col <
                                                 xvar.maze.cols):
            try:
                cell_value = xvar.maze.maze_matrix[xvar.row][xvar.col]
                x = xvar.col * xvar.maze.cell_size
                y = xvar.row * xvar.maze.cell_size

                # Check each wall using bit flags (from Border class)
                if cell_value & Border.NORTH:
                    draw_rectangle(xvar.maze, x, y,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.wall_width, xvar.maze.color)

                if cell_value & Border.SOUTH:
                    draw_rectangle(xvar.maze, x, y + xvar.maze.cell_size,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.wall_width, xvar.maze.color)

                if cell_value & Border.WEST:
                    draw_rectangle(xvar.maze, x, y, xvar.maze.wall_width,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.color)

                if cell_value & Border.EAST:
                    draw_rectangle(xvar.maze, x + xvar.maze.cell_size, y,
                                   xvar.maze.wall_width,
                                   xvar.maze.cell_size + xvar.maze.wall_width,
                                   xvar.maze.color)
                render_frame(xvar, xvar.maze)
                xvar.col += 1
                if xvar.col >= xvar.maze.cols:
                    xvar.col = 0
                    xvar.row += 1
            except IndexError:
                print(f"{xvar.col=} et {xvar.row=}")
        else:
            if xvar.solution.display:
                draw_42(xvar)
                xvar.mlx.mlx_loop_hook(xvar.mlx_ptr,
                                       xvar.solution.draw_solution_anim, xvar)
            else:
                xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, None, None)
                draw_42(xvar)
