import numpy as np
from .algo import generate_random_maze_prim
from .algo import generate_random_maze_eller
import random
from .algo import generate_random_maze_hunt_and_kill

MAZE_WALL = 1
MAZE_PATH = 0
MAZE_START = 3
MAZE_EXIT = 4
MAZE_TELEPORT = 6 



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
        self.flags = []  # List to store flag positions
        self.flags_collected = []  # List to keep track of collected flags
        self.visited_states = set()  # Set to keep track of visited states
        self.teleport_points = []  # List to store teleportation points


        # switch between different maze generation algorithms
        if generator_algorithm == "prim":
            generate_random_maze_prim(self)
        
        elif generator_algorithm == "eller":
            generate_random_maze_eller(self)

        elif generator_algorithm == "hunt-and-kill":
            generate_random_maze_hunt_and_kill(self)

        else:
            raise ValueError("Invalid generator_algorithm. Supported algorithms: 'prim', 'eller'")

            # Generate random flag positions
        self.generate_flags()
        self.generate_teleport_points()


    def generate_flags(self):
        # Here, we generate 3 flags, but you can change the number as needed.
        num_flags = 3
        available_positions = [(x, y) for x in range(self.width) for y in range(self.height) if self.matrix[x, y] == MAZE_PATH]
        self.flags = random.sample(available_positions, num_flags)

    def generate_teleport_points(self):
        num_teleport = 2
        available_positions = [(x, y) for x in range(self.width) for y in range(self.height) if self.matrix[x, y] == MAZE_PATH]
        self.teleport_points = random.sample(available_positions, num_teleport)

        # Place the teleportation destination for each teleportation point
        for i, teleport_point in enumerate(self.teleport_points):
            destination = self.teleport_points[1 - i]  # The destination will be the other teleportation point
            self.matrix[teleport_point[0], teleport_point[1]] = MAZE_TELEPORT
            self.matrix[destination[0], destination[1]] = MAZE_TELEPORT

    def is_teleport(self, x, y):
        # Check if the position is a teleportation point
        if self.matrix[x, y] == MAZE_TELEPORT:
            return x, y
        return None
    
    def is_wall(self, x, y):
        return self.matrix[x, y] == 1

    def is_exit(self, x, y):
        return (x, y) == self.exit

    def is_within_maze(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_reward(self, x, y):
        # Check if the agent hit a wall or went out of bounds
        if self.is_wall(x, y) or not self.is_within_maze(x, y):
            return -20.0  # Large negative reward for hitting a wall or going out of bounds

        # Check if the agent revisits a state
        current_state = (x, y)
        if current_state in self.visited_states:
            return -5.0  # Penalize revisiting states to encourage exploration

        # Mark the current state as visited
        self.visited_states.add(current_state)

        # Check if the agent reached a flag
        if current_state in self.flags and current_state not in self.flags_collected:
            return 1.0

        # Check if the agent reached the exit position with all flags collected
        if current_state == self.exit and len(self.flags_collected) == len(self.flags):
            return 10.0  # Positive reward for reaching the exit with all flags collected

        # Check if the agent reached the exit position without all flags collected
        if current_state == self.exit and len(self.flags_collected) < len(self.flags):
            return -10.0 * (len(self.flags) - len(self.flags_collected))  # Large negative reward for reaching the exit without all flags collected

        # Calculate the Manhattan distance to the nearest unvisited flag (D_flags)
        D_flags = float('inf')
        for flag in self.flags:
            if flag not in self.flags_collected:
                D = abs(flag[0] - x) + abs(flag[1] - y)
                D_flags = min(D_flags, D)

        # Calculate the Manhattan distance to the exit (D_exit)
        D_exit = abs(self.exit[0] - x) + abs(self.exit[1] - y)

        # Apply a time penalty to encourage the agent to find shorter paths
        time_penalty = -0.1

        # Define the reward based on the distances to flags and the exit
        reward = 0.5 * (1.0 / D_flags) + 0.5 * (1.0 / D_exit) + time_penalty

        # Apply teleportation reward adjustments
        teleport_reward = 0.0
        teleport_destination = self.is_teleport(x, y)
        if teleport_destination:
            # Provide a small positive reward for using teleportation
            teleport_reward = 0.1

        return reward + teleport_reward
