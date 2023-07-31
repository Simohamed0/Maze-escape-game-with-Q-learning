

# class for a dumb agent that just moves randomly
class DumbAgent:

    def __init__(self, maze):

        self.agent_position = self.maze.start
        self.agent_path = [self.agent_position]

    def move(self):
        # Move the agent randomly
        pass

    def get_position(self):
        return self.agent_position
    
    def get_path(self):
        return self.agent_path
