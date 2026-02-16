from mazegen import MazeManager

manager: MazeManager = MazeManager()
# maze: list[list[int]] = manager.get_maze(20, 15, False)
# solve: list[tuple[int, int]] = manager.solve_maze(maze, (0, 0), (19, 14))
# manager.create_output_file(maze, solve, 'maze.txt')
manager.create_complete_maze(20, 15, False, (0, 0), (19, 14), 'maze.txt')
