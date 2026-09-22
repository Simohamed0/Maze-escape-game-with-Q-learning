import random

from agent.agent import Agent


class DoubleQAgent(Agent):
    def __init__(self, maze, alpha=0.5, gamma=0.9, epsilon=0.1):
        super().__init__(maze)
        self.alpha, self.gamma, self.epsilon = alpha, gamma, epsilon
        self.q_table1, self.q_table2 = {}, {}

    @staticmethod
    def _q(table, state, action):
        return table.get(state, {}).get(action, 0.0)

    def get_action(self, x, y):
        actions = self.maze.valid_actions((x, y))
        if random.random() < self.epsilon:
            return random.choice(actions)
        state = self.maze.state((x, y))
        return max(actions, key=lambda action: self._q(self.q_table1, state, action) + self._q(self.q_table2, state, action))

    def move(self):
        state = self.maze.state(self.agent_position)
        self.action = self.get_action(*self.agent_position)
        next_position, reward, done = self.maze.step(self.agent_position, self.action)
        next_state = self.maze.state(next_position)
        if random.random() < 0.5:
            self._update(self.q_table1, self.q_table2, state, next_state, reward, done)
        else:
            self._update(self.q_table2, self.q_table1, state, next_state, reward, done)
        self.agent_position = next_position
        self.agent_path.append(next_position)
        return done

    def _update(self, update_table, evaluation_table, state, next_state, reward, done):
        target = reward
        if not done:
            actions = self.maze.valid_actions(next_state[0])
            best_action = max(actions, key=lambda action: self._q(update_table, next_state, action))
            target += self.gamma * self._q(evaluation_table, next_state, best_action)
        current = self._q(update_table, state, self.action)
        update_table.setdefault(state, {})[self.action] = current + self.alpha * (target - current)

    def get_q_table(self):
        return self.q_table1, self.q_table2
