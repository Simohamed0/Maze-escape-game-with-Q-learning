import numpy as np

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = np.zeros((width, height), dtype=int)
        self.start = (0, 0)
        self.exit = (width - 1, height - 1)
        self.generate_random_maze()  # Optionally, you can generate random mazes here.

    def generate_random_maze(self):
        # Your maze generation algorithm goes here
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
