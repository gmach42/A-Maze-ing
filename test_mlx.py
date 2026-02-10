import sys
from src.maze_generator import MazeGenerator
from mlx import Mlx
from src import Border
from src.solver import a_star_algorithm
from typing import Any,


class ImgData:
    """Structure for image data"""

    def __init__(self):
        self.img: Any = None  # mlx_new_image
        self.width: int = 0
        self.height: int = 0
        self.data: Any = None  # memoryview(int)
        self.sl: int = 0  # size line
        self.bpp: int = 0  # bits per pixel
        self.endian: int = 0


class XVar:
    """Structure for main vars"""

    def __init__(self):
        self.mlx: Mlx | None = None
        self.mlx_ptr: Any = None
        self.screen_w: int = 0
        self.screen_h: int = 0
        self.win: Any = None


def draw_line(
    xvar: XVar,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: int,
    line_width: int = 5,
):
    """
    Draw a line from (x0, y0) to (x1, y1) using [Bresenham's line algorithm](\
        https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)

    Color format: 0xAARRGGBB (e.g., 0xFFFFFFFF for white, 0xFFFF0000 for red)

    More information in README.md
    """

    if line_width == 0:
        raise ValueError("Line_width cannot be null")

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    # Get direction of the line with the sign sx, sy
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    # Get the slope of the line:
    # - If dy > dx, the line will be more vertical
    # - If dx > dy, the line will be more horizontal
    err = dx - dy

    while True:
        # Draw a filled square around each point
        draw_square(xvar, x0, y0, line_width, color)

        # If the destination is reached, stop the loop
        if x0 == x1 and y0 == y1:
            break

        # Check README.md / Bresenham's algorithm
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


# void	put_pixel_image(t_pixel pixel, char *str, int color)
# {
# 	unsigned char r;
# 	unsigned char g;
# 	unsigned char b;
# 	int len;

# 	len = WIN_LEN; /* En réalité, il s'agit de la longueur de votre image. Ici, mon image et ma fenêtre font la même taille */

# 	/* in this part you'll see how i decompose a decimal color in a third part decimal color rgb(255, 255, 255) */
# 	/* Dans cette partie, voici comment je decompose une couleur decimal en une couleur décimale en trois partie rgb(255, 255, 255) */
# 	r = (color >> 16) & 0xff;
# 	g = (color >> 8) & 0xff;
# 	b = color & 0xff;

# 	/* (pixel.x * 4) + (len * 4 * pixel.y) : cible le premier bit d'un pixel */
# 	str[(pixel.x * 4) + (len * 4 * pixel.y)] = b;
# 	str[(pixel.x * 4) + (len * 4 * pixel.y) + 1] = g;
# 	str[(pixel.x * 4) + (len * 4 * pixel.y) + 2] = r;
# 	str[(pixel.x * 4) + (len * 4 * pixel.y) + 3] = 0;
# }


def setup_image_buffer(xvar: XVar, width: int, height: int) -> ImgData:
    """Implement ImgData with a new image of dimension {width} x {height}"""
    image = ImgData()
    image.width = width
    image.height = height
    image.img = xvar.mlx.mlx_new_image(xvar.mlx_ptr, width, height)

    res = xvar.mlx.mlx_get_data_addr()
    image.data = res[0]
    image.sl = res[1]
    image.bpp = res[2]
    image.endian = res[3]


def put_pixel_to_image(img_data: ImgData, x: int, y: int, color: int) -> None:
    """Register pixel into img_data thanks to https://github.com/vgauther/mlx_img"""

    # Separate a decimal color into 3 part rgb (255, 255, 255) + alpha
    alpha = (color >> 24) & 0xff
    red = (color >> 16) & 0xff
    green = (color >> 8) & 0xff
    blue = color & 0xff

    if 0 <= x < img_data.width and 0 <= y < img_data.height:
        offset = y * img_data.sl + x * (img_data.bpp // 8)

        img_data.data[offset] = blue
        img_data.data[offset + 1] = green
        img_data.data[offset + 2] = red
        img_data.data[offset + 3] = alpha


def draw_maze_walls(
    xvar: XVar,
    maze: list[list[int]],
    cell_size: int = 50,
) -> None:
    """
    Draw walls around each cell using draw_line() and Border()
    """
    rows = len(maze)
    cols = len(maze[0])

    for row in range(rows):
        for col in range(cols):
            cell_value = maze[row][col]
            x = col * cell_size
            y = row * cell_size

            # Check each wall using bit flags (from Border class)
            if cell_value & Border.NORTH:
                draw_line(xvar, x, y, x + cell_size, y,
                          0xFFFFFFFF)

            if cell_value & Border.SOUTH:
                draw_line(xvar, x, y + cell_size, x + cell_size,
                          y + cell_size, 0xFFFFFFFF)

            if cell_value & Border.WEST:
                draw_line(xvar, x, y, x, y + cell_size,
                          0xFFFFFFFF)

            if cell_value & Border.EAST:
                draw_line(xvar, x + cell_size, y, x + cell_size,
                          y + cell_size, 0xFFFFFFFF)


def draw_square(xvar: XVar, x: int, y: int, size: int, color: int):
    for dy in range(-size, size + 1):
        for dx in range(-size, size + 1):
            xvar.mlx.mlx_pixel_put(xvar.mlx_ptr, xvar.win, x + dx, y +
                                   dy, color)


def draw_solution(xvar: XVar, solution: list[tuple], colors: Colors, cell_size: int = 50):
    x0, y0 = solution[0]
    x1, y1 = solution[len(solution) - 1]
    size_path = round(cell_size / 3)
    offset = round(cell_size / 2)

    draw_square(xvar, (x0 * cell_size + offset), (y0 * cell_size + offset), size_path, colors.start)
    draw_square(xvar, x1 * cell_size + offset, y1 * cell_size + offset, size_path, colors.end)
    for s in solution[1:len(solution) - 1]:
        y, x = s
        draw_square(xvar, x * cell_size + offset, y * cell_size + offset, size_path, colors.path)
    # TODO Finish draw solution (beginning + end + path)


def manage_close_1(xvar: XVar):
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)


def manage_key(key, xvar):
    print(f"Got key {key}: ", end="")

    if key == 65307:  # 'ESC'
        print("'ESC' key pressed, exciting...")
        xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)
        return 0
    return 0


def main():

    xvar = XVar()
    try:
        xvar.mlx = Mlx()
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)
    xvar.mlx_ptr = xvar.mlx.mlx_init()
    ret, xvar.screen_w, xvar.screen_h = xvar.mlx.mlx_get_screen_size(
        xvar.mlx_ptr
    )

    # Windows creation
    try:
        xvar.win = xvar.mlx.mlx_new_window(
            xvar.mlx_ptr, 1600, 1600, "MLX main win"
        )
        if not xvar.win:
            raise Exception("Can't create main window")
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)

    # Image #1
    xvar.img_1.img = xvar.mlx.mlx_new_image(xvar.mlx_ptr, 200, 200)
    if not xvar.img_1.img:
        raise Exception("Can't create image 1")

    xvar.img_1.width = 200
    xvar.img_1.height = 200
    xvar.img_1.data, xvar.img_1.bpp, xvar.img_1.sl, xvar.img_1.iformat = \
        xvar.mlx.mlx_get_data_addr(xvar.img_1.img)

    # Fill image #1
    for i in range(xvar.img_1.sl * 200):
        xvar.img_1.data[i] = 0x80

    for i in range(xvar.img_1.sl * 100):
        xvar.img_1.data[i] = 0xFF

    try:
        # Add some red pixels
        pixel_positions = [
            0 * 200 * 4,                   # top left
            (1 * 200 + 1) * 4,             # top left + 1
            (199 * 200 + 199) * 4,         # bottom right
            (198 * 200 + 198) * 4          # bottom right - 1
        ]

        for pos in pixel_positions:
            if pos < len(xvar.img_1.data) - 3:
                xvar.img_1.data[pos:pos+4] = (0xFFFF0000).to_bytes(4, 'little')
    except Exception as e:
        print(f"Error img1: {e}", file=sys.stderr)
        sys.exit(1)













    generator: MazeGenerator = MazeGenerator(15, 15)
    test_maze = generator.get_maze().tolist()
    print(test_maze)
    draw_maze_walls(xvar, test_maze)
    start = (0, 0)
    end = (14, 14)
    solution = a_star_algorithm(test_maze, start, end)

    # colors = Colors(
    #     start=hex(mc.to_hex(mc.CSS4_COLORS['red'], True)),
    #     end=hex(mc.to_hex(mc.CSS4_COLORS['magenta'], True)),
    #     path=hex(mc.to_hex(mc.CSS4_COLORS['mediumslateblue'], True))
    #     )
    # draw_solution(xvar, solution, colors)

    # event hooks
    xvar.mlx.mlx_key_hook(xvar.win, manage_key, xvar)
    # xvar.mlx.mlx_hook(xvar.win, 2, 1, manage_key_press, xvar)
    xvar.mlx.mlx_mouse_hook(xvar.win, 0, xvar)
    xvar.mlx.mlx_hook(xvar.win, 33, 0, manage_close_1, xvar)

    # Main loop
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    # Cleaning resources
    print("destroy win(s)")
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.win)
    print("destroy mlx")
    xvar.mlx.mlx_release(xvar.mlx_ptr)


if __name__ == "__main__":
    main()
