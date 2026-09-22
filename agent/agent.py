import random


class Agent:
    """Random baseline agent."""

    def __init__(self, maze):
        self.maze = maze
        self.time_list = []
        self.reset()

    def reset(self):
        self.maze.reset_episode()
        self.agent_position = self.maze.start
        self.agent_path = [self.agent_position]
        self.action = 0
    
    def get_position(self):
        return self.agent_position
    
    def get_path(self):
        return self.agent_path
    
    def get_next_position(self):
        x, y = self.agent_position
        if self.action == 0:  # Up
            x -= 1
        elif self.action == 1:  # Down
            x += 1
        elif self.action == 2:  # Left
            y -= 1
        elif self.action == 3:  # Right
            y += 1

        return (x, y) if self.maze.is_within_maze(x, y) else self.agent_position


    def get_action(self, x, y):
        actions = self.maze.valid_actions((x, y))
        return random.choice(actions) if actions else 4

    def set_position(self, x, y):
        self.agent_position = (x, y)

    def move(self):
        self.action = self.get_action(*self.agent_position)
        if self.action == 4:
            return False
        self.agent_position, _, done = self.maze.step(self.agent_position, self.action)
        self.agent_path.append(self.agent_position)
        return done
