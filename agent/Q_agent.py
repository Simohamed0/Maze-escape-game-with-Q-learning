import random

from agent.agent import Agent


class QAgent(Agent):
    def __init__(self, maze, alpha=0.5, gamma=0.9, epsilon=0.1):
        super().__init__(maze)
        self.alpha, self.gamma, self.epsilon = alpha, gamma, epsilon
        self.q_table = {}

    def _q(self, state, action):
        return self.q_table.get(state, {}).get(action, 0.0)

    def get_action(self, x, y):
        actions = self.maze.valid_actions((x, y))
        if random.random() < self.epsilon:
            return random.choice(actions)
        state = self.maze.state((x, y))
        return max(actions, key=lambda action: self._q(state, action))

    def move(self):
        current_state = self.maze.state(self.agent_position)
        self.action = self.get_action(*self.agent_position)
        next_position, reward, done = self.maze.step(self.agent_position, self.action)
        next_state = self.maze.state(next_position)
        next_actions = self.maze.valid_actions(next_position)
        target = reward if done else reward + self.gamma * max(self._q(next_state, action) for action in next_actions)
        current = self._q(current_state, self.action)
        self.q_table.setdefault(current_state, {})[self.action] = current + self.alpha * (target - current)
        self.agent_position = next_position
        self.agent_path.append(next_position)
        return done

    def get_q_table(self):
        return self.q_table
