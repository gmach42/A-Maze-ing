*This project has been created as part of the 42 curriculum by bfitte and gmach.*

# Description

**A-Maze-ing** is an interactive maze generation and visualization tool built in Python. Designed as part of the 42 curriculum, it generates mazes through a graphical interface powered by the MLX library.

The application generates perfect and imperfect mazes using algorithms like **Kruskal** and **Recursive Backtracking (DFS)**, while solving them with the __A* Pathfinding__ algorithm. A unique feature of this project is the preservation of a "42" shaped pattern within the maze structure.

With fully customizable dimensions, color themes, and animation speeds, users can explore the intricacies of algorithmic logic visually. Despite the limitations of the MLX library, the project prioritizes modular architecture, robust error handling, and comprehensive unit testing to ensure a stable and educational experience.

# Instructions

### Installation & Execution

To install dependencies and launch the application:
```bash
make install
make run
```

### Commands

| Command | Description |
| :--- | :--- |
| `make help` | Display all available make commands |
| `make test` | Run unit tests |
| `make clean` | Remove temporary files |
| `make clean-all` | Full cleanup (includes virtual environment) |
| `make lint` | Check code with flake 8 and mypy |
| `make lint-strict` | Check code with flake 8 and mypy in strict mode |
| `make keybind` | Display keybindings help message |

### Configuration

To customize the maze, edit the `config.txt` file and run `make run` again.
> For details on available options, see the **[Config file structure](#struct-and-format-of-config-file)** section.

## Features

### Core Functionality
- **Multiple Generation Algorithms**: Choose between **Kruskal** (perfect maze) and **Depth-First Search (DFS)** (recursive backtracker).
- **Smart Pathfinding**: Solves the maze using the __A* algorithm__ to find the optimal path.
- **Customizable Dimensions**: Define width, height, and entry/exit points via configuration.
- **"42" Shape Preservation**: Ensures a specific "42" pattern remains intact within the maze structure (when dimensions allow it).

### Visualization & Customization
- **Animated Generation**: Watch the maze being built and solved in real-time.
- **Color Themes**: Cycle through different color schemes for walls and the solution path.
- **Configurable Settings**: modifying the `config.txt` file allows for easy personalization of all parameters (See the [Config file structure](#struct-and-format-of-config-file) for more information).

### Interactive Controls
| Key | Action |
| :--- | :--- |
| `ESC` | Exit application |
| `r` | Regenerate a new maze |
| `a` | Switch generation algorithm |
| `d` | Toggle solution path visibility |
| `g` | Toggle "42" animation |
| `c` | Cycle wall colors |
| `s` | Cycle path colors |
| `h` | Show help message |

- **Window buttons**, clickable and with the same functionalities as the keybinds listed above, are also available for users who prefer mouse interaction.

## Technical Choices & Constraints

The uses of **MinilibX (MLX)** throughout this project has been an enjoyable and painfull experience at the same time. MLX is a minimal graphics library primarily designed for C, with limited Python support and documentation. To deliver a final display which satisfied our design goals, we made several architectural decisions and compromises:

- **Custom Animation Engine**: Implemented a frame-based rendering system from scratch, as MLX lacks native animation support.
- **Color Management**: Developed a custom palette system to handle color cycling within MLX's limited capabilities.
- **Performance Optimization**: Added an additional code layer to use the mlx base function to allow faster rendering and computing (Passing directly 16-bit color values instead of ARGB tuples for example).
- **Font Constraints**: Adapted UI design to fixed-size fonts, as scalable text is not supported.

> **Note**: We encountered and worked around several MLX limitations, such as inconsistent color formats (ABGR vs ARGB) and sparse documentation. Despite these challenges, we successfully created a visually appealing and interactive maze generator that meets our project goals.

### Struct and format of config file

The config.txt file allows only strictly defined values following the format `KEY=value`.

| Key | Type | Description |
| :--- | :--- | :--- |
| `WIDTH` | Integer | Maze width |
| `HEIGHT` | Integer | Maze height |
| `ENTRY` | `(x,y)` | Coordinates for maze entry point |
| `EXIT` | `(x,y)` | Coordinates for maze exit point |
| `OUTPUT_FILE` | String | Filename for maze output |
| `PERFECT` | Boolean | Toggle perfect maze generation (`true`/`false`) |
| `ANIMATION` | Boolean | Toggle generation and solution animation |
| `SPEED_ANIMATION` | String | Animation speed (`slow`, `medium`, `fast`) |
| `SEED` | String | Custom seed for generation (use `'false'` for random) |

## Algorithms & Logic

### 1. Maze Generation
We implemented two distinct algorithms to generate mazes, each offering unique visual and structural characteristics.

#### **Kruskal's Algorithm** (Randomized)
*Creates a "perfect" maze with a Minimum Spanning Tree structure.*

Kruskal's algorithm is a "greedy" approach that treats every cell as a separate set and progressively merges them by breaking walls until all cells belong to a single set. This guarantees a perfect maze where exactly one path exists between any two cells.

**Logic & Implementation:**

1.  **Wall Collection**: The algorithm begins by identifying all possible "breakable" walls between adjacent cells, strictly excluding any walls that form the protected "42" shape.
2.  **Randomization**: This list of potential walls (`walls_to_break`) is shuffled randomly to ensure the generated maze is non-deterministic and unique every run.
3.  **Set Union (The "Boss" System)**: For each wall in the list, we check the "boss" (set identifier) of the two cells separated by that wall.
    - **Wall Breaking**: If the cells have different bosses (meaning they are not yet connected), we call a `union` function to merge their sets and delete the wall.
    - **Cycle Prevention**: If both cells already share the same boss, the wall is left intact to prevent creating loops or cycles.


<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:640/format:webp/1*t3EZxEDdnzwhaYzCARzzUA.gif" width="300" alt="Kruskal's Algorithm">
    <br>
  <em>Kruskal's Algorithm</em>
</p>


#### **Depth-First Search (DFS)** (Recursive Backtracker)
*Creates a maze with long, winding corridors and fewer dead ends.*

DFS, often called the "recursive backtracker," is a randomized algorithm that explores as deep as possible along each branch before backtracking. It mimics a human blindly exploring a maze and marking their path.

**Logic & Implementation:**

1.  **Initialization**: We start at a designated cell, mark it as visited, and push it onto a stack.
2.  **Navigation**: The algorithm peeks at the top of the stack to identify the current active cell.
3.  **Neighbor Selection**: It identifies all valid adjacent neighbors (North, South, East, West) that have **not** been visited and are not part of the "42" structure.
4.  **Wall Removal**:
    - If unvisited neighbors exist, one is chosen at random. The wall between the current cell and the neighbor is removed, the neighbor is marked visited and pushed to the stack.
    - This creates a long, continuous corridor.
5.  **Backtracking**: If no unvisited neighbors exist (a dead end), the algorithm pops the current cell from the stack and backtracks to the previous one, repeating the process until the stack is empty.

<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*unQanD3lFwpajj6lsJVw8g.gif" width="300" alt="Depth-First Search Algorithm">
    <br>
  <em>Depth-First Search Algorithm</em>
</p>

### 2. Pathfinding: A* Algorithm
To solve the maze, we utilize __A* (A-Star)__, a powerful search algorithm that finds the shortest path by combining actual cost with a [heuristic](https://en.wikipedia.org/wiki/Heuristic_(computer_science)) estimate. The heuristic function chosen is the [Manhattan Distance](https://en.wikipedia.org/wiki/Taxicab_geometry). During the processing of the algorithm, each cell has a value assigned to it based on the following formula:

- **Cost Function :** $f(n) = g(n) + h(n)$
    - $f(n)$: Total estimated cost of the cheapest solution through node $n$.
    - $g(n)$: Exact cost from start to current cell.
    - $h(n)$: Heuristic estimated cost to goal (using **Manhattan Distance**).
- **Logic**: The algorithm prioritizes exploring cells with the lowest $f(n)$, ensuring the most promising paths are checked first.

<p align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Manhattan_distance.svg/960px-Manhattan_distance.svg.png" width="300" alt="Manhattan Distance">
        <br>
        <em>Manhattan Distance in red, blue and yellow</em>
        <br>
        <em>Green represents the Euclidean distance</em>
      </td>
      <td align="center">
        <img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*oais-M3DTKygQKO6cpszXQ.gif" width="300" alt="A* Algorithm">
        <br>
        <em>A* Algorithm visualization</em>
      </td>
    </tr>
  </table>
</p>


> **Resources**: [Bitwise Operations](https://github.com/Tutors42Lyon/bitwise_operations/tree/main) | [Manhattan Distance](https://en.wikipedia.org/wiki/Taxicab_geometry) | [Heuristic](https://en.wikipedia.org/wiki/Heuristic_(computer_science))

## Architecture & Reusability

The codebase follows a strict **modular architecture**:

- **Standalone Mazegen Module**: `mazegen` module can be used independently for maze generation and solving, making it reusable for other projects (like for a Pacman project for example)
- **Config-Driven**: The system is fully data-driven via `config.txt`, making it adaptable without code changes.
- **Type Safety**: Extensive use of Python type hints and `mypy` strict mode ensures code reliability.

### Using Mazegen as a Library

The `mazegen` module is designed to be able to be used independently and can be imported into other projects:

```python
from mazegen import MazeManager

# Generate a complete maze with solution and save it to a file
maze_manager = MazeManager()
maze_manager.create_complete_maze(height=20, width=10, perfect=True, start=(0, 0), end=(19, 9), output_file="maze.txt", seed=None, algo=1)
```

To install the module, you can use pip (in a virtual environment if desired):
```bash
pip install ./mazegen.tar.gz
```

For complete documentation and examples, see the **[mazegen README](src/mazegen/README.md)**.

## Team & Project Management

**Project Context**: 42 School Curriculum
**Development Time**: ~7 days

### Task Distribution

| **Bruno (`bfitte`)** | **Gildas (`gmach`)** |
| :--- | :--- |
| Maze Generation Logic | A* Pathfinding Logic |
| UI & Button System | Event & Input System |
| Config Parsing | Color Management |
| Animation System | Architecture & Refactoring |

### Retrospective

**Successes:**
- Successfully delivered all planned features, including bonus UI elements like clickable buttons (o7 changing button color on click).
- Overcame significant limitations in the MLX library to build a robust rendering engine.

**Areas for Improvement:**
- **Initial Planning**: We started with a monolithic structure and had to refactor heavily midway. A more detailed architecture plan upfront would have saved time.
- **Scope Management**: We had many ambitious ideas but had to cut some due to time constraints and the complexity of working with MLX.

## Resources & Tools

We chose **MinilibX (MLX)** over ASCII rendering because, although more challenging to work with, it allows for a more engaging and visually appealing result and we liked the challenge!

- **Graphics**: [MinilibX Documentation](https://harm-smits.github.io/42docs/libs/minilibx) / [Bresenham's Line Algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)
- **Algorithms**: [Maze Generation (Wiki)](https://en.wikipedia.org/wiki/Maze_generation_algorithm) / [A* Search (Wiki)](https://en.wikipedia.org/wiki/A*_search_algorithm) / [A* Algorithm in python](https://levelup.gitconnected.com/a-star-a-search-for-solving-a-maze-using-python-with-visualization-b0cae1c3ba92)/ [Heuristics](https://en.wikipedia.org/wiki/Heuristic_(computer_science)) / [Border's Idea](https://realpython.com/python-maze-solver/)

### AI Usage
Generative AI tools were used during development for:
- Writing and enhancing technical documentation (including this README).
- Clarifying obscure MLX behaviors and C-to-Python binding issues.
- Generating certains docstrings (particurly for the complex class docstrings)
- Helping for the structuring of the codebase.
