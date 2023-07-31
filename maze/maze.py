import numpy as np
import random

MAZE_WALL = 1
MAZE_PATH = 0
MAZE_START = 3
MAZE_EXIT = 4


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = np.full((width, height), MAZE_WALL, dtype=int)
        self.start = 0,1
        self.exit = width - 1, height - 2
        self.agent_position = self.start
        self.agent_path = [self.agent_position]
        self.difficulty = 1
        self.generate_random_maze()  # Optionally, you can generate random mazes here.

    def generate_random_maze(self):
        def get_neighbors(cell):
            x, y = cell
            neighbors = [(x+dx, y+dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
            random.shuffle(neighbors)
            return [neighbor for neighbor in neighbors if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height]

        def dfs(cell):
            self.matrix[cell] = MAZE_WALL

            for neighbor in get_neighbors(cell):
                x, y = neighbor
                if self.matrix[x, y] == MAZE_WALL:
                    nx, ny = (x + cell[0]) // 2, (y + cell[1]) // 2
                    self.matrix[nx, ny] = MAZE_PATH
                    dfs(neighbor)

        dfs(self.start)

        
        # Restore the walls on the perimeter of the maze
        self.matrix[:, 0] = MAZE_WALL
        self.matrix[:, -1] = MAZE_WALL
        self.matrix[0, :] = MAZE_WALL
        self.matrix[-1, :] = MAZE_WALL

        # Set the start and exit cells
        self.matrix[self.start] = MAZE_START
        self.matrix[self.exit] = MAZE_EXIT


    def is_wall(self, x, y):
        return self.matrix[x, y] == 1

    def is_exit(self, x, y):
        return (x, y) == self.exit

    def is_within_maze(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def update_agent_position(self, x, y):
        # Update the agent's position in the maze
        pass

    # Other utility methods for interacting with the maze can be added here
