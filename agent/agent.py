import random

# class for a dumb agent that just moves randomly
class Agent:

    def __init__(self, maze):

        self.agent_position = maze.start
        self.agent_path = [self.agent_position]
        self.action = 0
        self.maze = maze

    def get_action(self, x, y):
        # Get the agent's next action
        return self.action
    
    def get_position(self):
        return self.agent_position
    
    def get_path(self):
        return self.agent_path
    
    def get_next_position(self):
        # Get the agent's next position without actually updating the agent's position
        x, y = self.agent_position
        if self.action == 0:  # Up
            x -= 1
        elif self.action == 1:  # Down
            x += 1
        elif self.action == 2:  # Left
            y -= 1
        elif self.action == 3:  # Right
            y += 1

        # Check if the next position is within the maze boundaries
        if self.maze.is_within_maze(x, y):
            return x, y
        else:
            # If the next position is out of bounds, return the current position
            return self.agent_position


    def get_action(self, x, y):
        # Get all possible actions (directions) the agent can take
        possible_actions = []
        if self.maze.is_within_maze(x - 1, y) and not self.maze.is_wall(x - 1, y):
            possible_actions.append(0)  # Up
        if self.maze.is_within_maze(x + 1, y) and not self.maze.is_wall(x + 1, y):
            possible_actions.append(1)  # Down
        if self.maze.is_within_maze(x, y - 1) and not self.maze.is_wall(x, y - 1):
            possible_actions.append(2)  # Left
        if self.maze.is_within_maze(x, y + 1) and not self.maze.is_wall(x, y + 1):
            possible_actions.append(3)  # Right

        # Randomly choose one of the available actions
        if possible_actions:
            return random.choice(possible_actions)
        else:
            # If no available actions, stay in place (action 4)
            return 4
