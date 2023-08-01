import numpy as np
import random
from .algo import generate_random_maze_prim


MAZE_WALL = 1
MAZE_PATH = 0
MAZE_START = 3
MAZE_EXIT = 4



class Maze:
    def __init__(self, width, height, generator_algorithm="prim"):
        self.width = width
        self.height = height
        self.matrix = np.full((width, height), MAZE_WALL, dtype=int)
        self.start = 0,1
        self.exit = width - 1, height - 2
        self.agent_position = self.start
        self.agent_path = [self.agent_position]
        self.difficulty = 1
        
        # switch between different maze generation algorithms
        if generator_algorithm == "prim":
            generate_random_maze_prim(self)

    
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
