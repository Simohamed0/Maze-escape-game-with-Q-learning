import random

# class for a dumb agent that just moves randomly
class DumbAgent:

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
