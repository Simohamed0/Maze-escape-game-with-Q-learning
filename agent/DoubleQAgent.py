# Parameters
alpha = 0.5
gamma = 0.5
exploration = 0.1
import random
import numpy as np
from agent.agent import Agent


class DoubleQAgent(Agent):

    def __init__(self, maze):
        super().__init__(maze)
        self.q_table1 = {}  # First Q-table
        self.q_table2 = {}  # Second Q-table
        self.time_list = []

    def set_position(self, x, y):
        self.agent_position = x, y

    def move(self):
        current_state = self.agent_position
        self.action = self.get_action(*current_state)
        next_position = self.get_next_position()

        # Check if the next position is not a wall
        if not self.maze.is_wall(*next_position):
            self.agent_position = next_position

        new_state = self.agent_position

        # Randomly choose which Q-table to update
        if random.uniform(0, 1) < 0.5:
            self.update_q_value(self.q_table1, current_state, new_state)
        else:
            self.update_q_value(self.q_table2, current_state, new_state)

        self.agent_path.append(self.agent_position)

    def get_action(self, x, y):
        possible_actions = self.get_possible_actions(x, y)

        # Randomly choose one of the available actions based on epsilon-greedy policy
        if random.uniform(0, 1) < exploration:
            return random.choice(possible_actions)
        else:
            return self.get_best_action(x, y)

    def get_possible_actions(self, x, y):
        possible_actions = []
        if self.maze.is_within_maze(x - 1, y) and not self.maze.is_wall(x - 1, y):
            possible_actions.append(0)  # Up
        if self.maze.is_within_maze(x + 1, y) and not self.maze.is_wall(x + 1, y):
            possible_actions.append(1)  # Down
        if self.maze.is_within_maze(x, y - 1) and not self.maze.is_wall(x, y - 1):
            possible_actions.append(2)  # Left
        if self.maze.is_within_maze(x, y + 1) and not self.maze.is_wall(x, y + 1):
            possible_actions.append(3)  # Right
        return possible_actions

    def get_best_action(self, x, y):
        # Get the action with the highest Q-value for the current state (exploitation)
        state = (x, y)
        possible_actions = self.get_possible_actions(x, y)
        if not possible_actions:
            # If no Q-values are available for the current state, explore (choose randomly)
            return random.choice([0, 1, 2, 3])

        # Get the Q-values from both Q-tables and average them
        q_values1 = [self.q_table1.get(state, {}).get(action, 0) for action in possible_actions]
        q_values2 = [self.q_table2.get(state, {}).get(action, 0) for action in possible_actions]
        avg_q_values = np.mean([q_values1, q_values2], axis=0)

        return possible_actions[np.argmax(avg_q_values)]

    def update_q_value(self, q_table, current_state, new_state):
        current_q = q_table.get(current_state, {}).get(self.action, 0)

        # Get the best action for the new state using the other Q-table
        if random.uniform(0, 1) < 0.5:
            best_action_new_state = self.get_best_action(*new_state)
            max_q_new_state = self.q_table1.get(new_state, {}).get(best_action_new_state, 0)
        else:
            best_action_new_state = self.get_best_action(*new_state)
            max_q_new_state = self.q_table2.get(new_state, {}).get(best_action_new_state, 0)

        updated_q = current_q + alpha * (self.maze.get_reward(*new_state) + gamma * max_q_new_state - current_q)

        # Update the Q-table with the new Q-value
        if current_state not in q_table:
            q_table[current_state] = {}
        q_table[current_state][self.action] = updated_q

    def get_q_table(self):
        return self.q_table1, self.q_table2

    def display_q_tables(self):
        # Display the Q-tables as 2D grids
        print("Q-table 1:")
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                print("{:6.2f}".format(self.q_table1.get((x, y), {}).get(0, 0)), end=" ")
            print()
        print()

        print("Q-table 2:")
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                print("{:6.2f}".format(self.q_table2.get((x, y), {}).get(0, 0)), end=" ")
            print()
        print("--------------------------------------------------")


