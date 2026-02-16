*This project has been created as part of the 42 curriculum by bfitte and gmach.*

# Description

This module is a part of the A-Maze-ing project from the 42-Curriculum but can also be use as a stand alone for any maze related program.

It create a txt file with a maze in hexadecimal format representing the walls of the maze. Two algortihm are available to create the maze, the Kullback algorithm and the Depth First Search algorithm. The Kullback algorithm is a randomized algorithm that creates a maze by randomly removing walls, while the Depth First Search algorithm creates a maze by exploring the maze in a depth-first manner. The solver algorithm used is the A* algorithm, which is a popular pathfinding algorithm that uses heuristics to find the shortest path between two points in a maze.

The output file contains the maze in hexadecimal format, followed by the entry and exit coordinates, and finally the solution path as a sequence of directions (S for South, E for East, N for North, W for West). A 42 obstacle is present in the maze as long as the maze is big enough (at least 7 x 9)

# Instructions

To install the package, you can use the following command:
```
pip install mazegen.tar.gz
```

To build the package, you can use the following commands:
```
pip install build
python3 -m build
```

## Usage example

You can use this module in two ways, either use a all-in-one method to create the maze, solve it and print the whole thing to an output file or use each component separately.

### Defining the parameters for the maze:

```py
from mazegen import MazeManager

# Create a MazeManager
maze_manager = MazeManager()

# Define the parameters for the maze, here are some examples:
height: int = 10  # number of rows in the maze
width: int = 10  # number of columns in the maze
perfect: bool = True  # whether the maze is perfect or not
start: tuple[int, int] = (0, 0)  # starting position
end: tuple[int, int] = (9, 9)  # ending position
output_file: str = "maze.txt"  # name of the output file
seed: int | None = None  # Optional random seed for maze generation, if None, a random seed will be used
# Optional algorithm to use for maze generation, 1 for Kullback, 2 for Depth First (default is Kullback)
algo: int | None = 1
```
### All-in-one method:
```py
# Create a complete maze and print it to an output file
maze_manager.create_complete_maze(height, width, perfect, start, end, output_file, seed, algo)
```

### Using each component separately:
```py
# Create a maze
maze: list[list[int]] = maze_manager.create_maze(height, width, perfect, seed, algo)

# Solve the maze using the A* algorithm
solution: list[tuple[int, int]] = maze_manager.solve_maze(maze, start, end)

# Print the maze to an output file
maze_manager.create_output_file(maze, solution, output_file)
```

### Output file example
The output file will contain the maze in hexadecimal format, followed by the entry and exit coordinates, and finally the solution path as a sequence of directions (S for South, E for East, N for North, W for West). Here is an example of what the output file might look like (10 x 10 maze with entry at (0, 0) and exit at (9, 9)):

```txt
BB97979117
A80787EAC3
AAC38556D6
86FAABFFFB
83FC4057FA
EAFFFAFFFA
9453FEFD52
857EFBFFFA
A9797AB93A
C4545446C6

0,0
9,9
SSSSESSWSSSEEEEEEENESE
```

# Resources

As stated before, this module is a part of the A-Maze-ing project from the 42-Curriculum, you can find more information about the project and its other components on the GitHub repository:

- [A-Maze-ing project](https://github.com/gmach42/A-Maze-ing)

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/242624862/550350568-67eef766-2b61-4fd4-8c38-cff22b0ad70e.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzEyMzM3NDEsIm5iZiI6MTc3MTIzMzQ0MSwicGF0aCI6Ii8yNDI2MjQ4NjIvNTUwMzUwNTY4LTY3ZWVmNzY2LTJiNjEtNGZkNC04YzM4LWNmZjIyYjBhZDcwZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjE2JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIxNlQwOTE3MjFaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01ZmNkM2NmYTVkYWM2NjExM2Y5MzllM2Y3ZDBkNDBlZDJhODgwMjQ3ZDI1NmEyZjg0MjQ2MThlZTM4NzRhYjQ3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.kESrFkQI2_s40C1VSfpo9HTAMMnZTOwb_Ek0VuO58a4" width="400" alt="a-maze-ing maze example" />
    <br>
  <em>Example of a maze generated through A-Maze-ing with MLX display</em>
</p>

