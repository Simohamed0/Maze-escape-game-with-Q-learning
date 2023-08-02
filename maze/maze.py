import numpy as np
from .algo import generate_random_maze_prim
from .algo import generate_random_maze_eller
import random
from .algo import generate_random_maze_hunt_and_kill

MAZE_WALL = 1
MAZE_PATH = 0
MAZE_START = 3
MAZE_EXIT = 4



class Maze:
    def __init__(self, width, height, generator_algorithm="prim"):
        self.width = width
        self.height = height
        self.matrix = np.full((width, height), MAZE_WALL, dtype=int)
        self.start = 0,0
        self.exit = width - 1, height - 1
        self.agent_position = self.start
        self.agent_path = [self.agent_position]
        self.difficulty = 1
        
        # switch between different maze generation algorithms
        if generator_algorithm == "prim":
            generate_random_maze_prim(self)
        
        elif generator_algorithm == "eller":
            generate_random_maze_eller(self)

        elif generator_algorithm == "hunt-and-kill":
            generate_random_maze_hunt_and_kill(self)

        else:
            raise ValueError("Invalid generator_algorithm. Supported algorithms: 'prim', 'eller'")


    
    def is_wall(self, x, y):
        return self.matrix[x, y] == 1

    def is_exit(self, x, y):
        return (x, y) == self.exit

    def is_within_maze(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_reward(self, x, y):
        # Check if the agent reached the exit position
        if (x, y) == self.exit:
            return 100.0  # Positive reward for reaching the exit
        # Check if the agent hit a wall or went out of bounds
        if self.is_wall(x, y) or not self.is_within_maze(x, y):
            return -10.0  # Large negative reward for hitting a wall or going out of bounds
        return -0.1  # Small negative reward for each step the agent takes

    def get_neighbors(self, x, y):
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [(nx, ny) for nx, ny in neighbors if self.is_within_maze(nx, ny)]

    def generate_random_maze_hunt_and_kill(self):
        # Step 1: Choose a random starting location
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.matrix[start_x, start_y] = MAZE_PATH

        # Helper function to check if a cell has an unvisited neighbor
        def has_unvisited_neighbor(x, y):
            return any(self.matrix[nx, ny] == MAZE_PATH for nx, ny in self.get_neighbors(x, y))

        # Helper function to get a random visited neighbor
        def get_random_visited_neighbor(x, y):
            visited_neighbors = [(nx, ny) for nx, ny in self.get_neighbors(x, y) if self.matrix[nx, ny] == MAZE_PATH]
            return random.choice(visited_neighbors) if visited_neighbors else None

        # Step 2: Perform a random walk until the current cell has no unvisited neighbors
        current_x, current_y = start_x, start_y
        while has_unvisited_neighbor(current_x, current_y):
            current_x, current_y = random.choice(self.get_neighbors(current_x, current_y))
            self.matrix[current_x, current_y] = MAZE_PATH

        # Step 3 and 4: Enter "hunt" mode and repeat steps 2 and 3 until the entire grid is scanned
        while not np.all(self.matrix == MAZE_PATH):
            # Find a random unvisited cell adjacent to a visited cell
            x, y = None, None
            for i in range(self.width):
                for j in range(self.height):
                    if self.matrix[i, j] == MAZE_WALL and has_unvisited_neighbor(i, j):
                        x, y = i, j
                        break
                if x is not None and y is not None:
                    break

            if x is None or y is None:
                # If no unvisited cell with visited neighbors is found, the maze is complete
                break

            # Perform a random walk starting from the chosen unvisited cell
            while has_unvisited_neighbor(x, y):
                x, y = random.choice(self.get_neighbors(x, y))
                self.matrix[x, y] = MAZE_PATH

