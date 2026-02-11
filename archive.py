def draw_line(
    img_data: ImgData,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: int,
    line_width: int = 6,
) -> None:
    """
    Draw a line from (x0, y0) to (x1, y1) using [Bresenham's line algorithm](\
        https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)

    Color format: 0xAARRGGBB (e.g., 0xFFFFFFFF for white, 0xFFFF0000 for red)

    More information in README.md

    Unused since we do not use mlx_pixel_put anymore
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
        draw_rectangle(img_data, x0, y0, line_width, color)

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
