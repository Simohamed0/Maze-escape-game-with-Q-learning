import numpy as np
import random

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = np.zeros((width, height), dtype=int)
        self.start = random.randint(0, width - 1), 0
        self.exit = random.randint(0, width - 1), height - 1
        self.agent_position = self.start
        self.agent_path = [self.agent_position]
        self.difficulty = 1
        self.generate_random_maze()  # Optionally, you can generate random mazes here.

    # function to generate random maze
    def generate_random_maze(self):
        # using rando
        pass


    def is_wall(self, x, y):
        return self.maze[x, y] == 1

    def is_exit(self, x, y):
        return (x, y) == self.exit

    def is_within_maze(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def update_agent_position(self, x, y):
        # Update the agent's position in the maze
        pass

    # Other utility methods for interacting with the maze can be added here
