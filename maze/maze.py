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
        self.start = 0,0
        self.exit = width - 1, height - 1
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

    def get_reward(self, x, y):
        # Check if the agent reached the exit position
        if (x, y) == self.exit:
            return 1.0  # Positive reward for reaching the exit
        # Check if the agent hit a wall or went out of bounds
        if self.is_wall(x, y) or not self.is_within_maze(x, y):
            return -10.0  # Large negative reward for hitting a wall or going out of bounds
        return -0.1  # Small negative reward for each step the agent takes
