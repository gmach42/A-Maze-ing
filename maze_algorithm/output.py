def output_maze(maze_matrix: list[list[int]],
                sol_matrix: list[tuple[int, int]]) -> None:
    """Output the maze and its solution to a output_maze.txt file."""
    with open("output_maze.txt", "w") as f:
        # Maze in hexadecimal format
        f.write(maze_to_string(maze_matrix) + "\n")
        # Start
        f.write('\n' + str(sol_matrix[0]).strip('()').replace(' ', '') + "\n")
        # End
        f.write(str(sol_matrix[-1]).strip('()').replace(' ', '') + "\n")
        # Solution in cardinal direction
        f.write(sol_cardinal_direction(sol_matrix) + "\n")


def sol_cardinal_direction(sol_matrix: list[tuple[int, int]]) -> str:
    """transform the path into a string of direction"""

    # iterate on the whole path except last node
    if not sol_matrix:
        raise ValueError("No matrix found")
    directions: str = ""
    for i in range(len(sol_matrix) - 1):
        curr_row, curr_col = sol_matrix[i]
        next_row, next_col = sol_matrix[i + 1]

        # Compare row change
        if next_row < curr_row:
            directions += "N"
        elif next_row > curr_row:
            directions += "S"
        # Compare col change
        elif next_col < curr_col:
            directions += "W"
        elif next_col > curr_col:
            directions += "E"

    return directions


def maze_to_string(maze_matrix: list[list[int]]) -> str:
    """transform the maze into a string in hexadecimal format"""
    return "\n".join("".join(format(cell, "X") for cell in row)
                     for row in maze_matrix)
