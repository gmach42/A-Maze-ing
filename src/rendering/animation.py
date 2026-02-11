from src.core import XVar
from src.solver import Border
from .renderer import draw_rectangle, render_frame


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
