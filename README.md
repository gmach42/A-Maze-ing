*This project has been created as part of the 42 curriculum by bfitte and gmach.*

# Description
A generator of mazes, possibly perfect ones, that writes the result to a file using a hexadecimal wall representation. It also provides a visual
 representation of the maze and some animation possibilities.
# Instructions
# Resources
## Usage examples
## Feature list
## Technical choices
### Struct and format of config file
### Maze generation algorithm chosen

A heap queue (also called a priority queue) is a special data structure that allows quick access to the smallest (min-heap) or largest (max-heap) element

Taxicab geometry or Manhattan geometry is geometry where the familiar Euclidean distance is ignored, and the distance between two points is instead defined to be the sum of the absolute differences of their respective Cartesian coordinates, a distance function (or metric) called the taxicab distance, Manhattan distance, or city block distance.

#### Kruskal algorithm:
Kruskal's algorithm is a "greedy" algorithm typically used to find a Minimum Spanning Tree. In the context of maze generation, it treats every cell as a separate set and progressively merges them by breaking walls until all cells belong to a single set, ensuring a perfect maze (one path between any two cells).

Logic and Implementation:

Wall Collection: The algorithm begins by creating a list of all possible "breakable" walls between adjacent cells, strictly excluding any walls associated with the "42" shape.

Randomization: The list of walls (walls_to_broke) is shuffled randomly to ensure the maze structure is non-deterministic.

Set Union (The "Boss" System): For each wall in the shuffled list, the algorithm checks the "boss" of the two cells separated by that wall.

Wall Breaking: If the two cells have different bosses (meaning they are not yet connected), the algorithm calls a union function to merge the sets. The wall between the two cells is then deleted.

Cycle Prevention: If both cells already share the same boss, the wall is left intact to prevent the creation of loops/cycles within the maze.

#### Depth-First Search (DFS)
The Depth-First Search algorithm, often called the "recursive backtracker," is a randomized algorithm that explores as deep as possible along each branch before backtracking.

Logic and Implementation:

Initialization: The algorithm starts with a designated start_cell, marks it as visited, and pushes it onto a stack.

Navigation: It peeks at the top of the stack to identify the current cell.

Neighbor Selection: The algorithm identifies all adjacent neighbors (North, South, East, West) that have not been visited and are not part of the protected "42" shape.

Wall Removal: If unvisited neighbors are available, one is chosen at random (rand.choice). The wall between the current cell and the chosen neighbor is deleted, the neighbor is marked as visited, and it is pushed onto the stack.

Backtracking: If no unvisited neighbors exist, the algorithm pops the current cell from the stack and repeats the process from the previous cell. The loop terminates when the stack is empty.

#### A* algorithm:
The way A* works is that it assigns a cost to each of the cells of the maze and the algorithm selects the SolutionPath with minimum cost. The cost of a cell (n) has two parts and is defined as:
```math
f(n) = g(n)+h(n)
```
Where f(n) is the total cost to reach the cell n and g(n) and h(n) are defined as:

g(n) → It is the actual cost to reach cell n from the start cell.

h(n) → It is the heuristic cost to reach to the goal cell from cell n. It is the estimated cost to reach the goal cell from cell n.

from [A* algorithm](https://levelup.gitconnected.com/a-star-a-search-for-solving-a-maze-using-python-with-visualization-b0cae1c3ba92)

Thought about doing an adjacency matrix but using a Border approach seems more practicable in our case

Binary operator:
https://github.com/Tutors42Lyon/bitwise_operations/tree/main

```python
function A_Star(start, goal, h)
    // The set of discovered nodes that may need to be (re-)expanded.
    // Initially, only the start node is known.
    // This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet := {start}

    // For node n, cameFrom[n] is the node immediately preceding it on the cheapest SolutionPath from the start
    // to n currently known.
    cameFrom := an empty map

    // For node n, gScore[n] is the cost of the cheapest SolutionPath from start to n currently known.
    gScore := map with default value of Infinity
    gScore[start] := 0

    // For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    // how cheap a SolutionPath could be from start to finish if it goes through n.
    fScore := map with default value of Infinity
    fScore[start] := h(start)

    while openSet is not empty
        // This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        current := the node in openSet having the lowest fScore[] value
        if current = goal
            return reconstruct_SolutionPath(cameFrom, current)

        openSet.Remove(current)
        for each neighbor of current
            // d(current,neighbor) is the weight of the edge from current to neighbor
            // tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore := gScore[current] + d(current, neighbor)
            if tentative_gScore < gScore[neighbor]
                // This SolutionPath to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] := current
                gScore[neighbor] := tentative_gScore
                fScore[neighbor] := tentative_gScore + h(neighbor)
                if neighbor not in openSet
                    openSet.add(neighbor)

    // Open set is empty but goal was never reached
    return failure
```
### Code reusability
### Team & project management

#### Task distribution

**Bruno**
- Maze Generation Algorithm
- Buttons
- Parsing
- Animations
- MazeUi

**Gildas**
- A* Pathfinding Algorithm
- Keybind Managment
- Color Manager
- Drawing functions
- Project Structuration


#### Role of each member
#### Planning and evolution
#### Good points and points to improve
#### Tools used and why

Algorithm used to draw a line ([Bresenham's line algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm))
```py
plotLine(x0, y0, x1, y1)
    dx = abs(x1 - x0)
    sx = x0 < x1 ? 1 : -1
    dy = -abs(y1 - y0)
    sy = y0 < y1 ? 1 : -1
    error = dx + dy

    while true
        plot(x0, y0)
        e2 = 2 * error
        if e2 >= dy
            if x0 == x1 break
            error = error + dy
            x0 = x0 + sx
        end if
        if e2 <= dx
            if y0 == y1 break
            error = error + dx
            y0 = y0 + sy
        end if
    end while
```


### Advanced features (multiple algortithms, display options, animation)
# IA
