import random
import numpy as np
from agent.agent import Agent

    
alpha = 0.1  # Learning rate, controls the impact of new information on Q-values
gamma = 0.3  # Discount factor, balances immediate and future rewards
exploration = 0.1  # Exploration rate, controls how often the agent explores instead of exploiting




class QAgent(Agent):

    def __init__(self, maze):
        super().__init__(maze)
        # initialize the Q-table 
        self.q_table = {}
        self.time_list = []



    def move(self):
        current_state = self.agent_position
        self.action = self.get_action(*current_state)
        next_position = self.get_next_position()

        # Check if the next position is not a wall
        if not self.maze.is_wall(*next_position):
            self.agent_position = next_position

        new_state = self.agent_position
        self.update_q_value(current_state, new_state)
        self.agent_path.append(self.agent_position)

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

        # Randomly choose one of the available actions based on epsilon-greedy policy
        if random.uniform(0, 1) < exploration:
            return random.choice(possible_actions)
        else:
            return self.get_best_action(x, y)



    def get_best_action(self, x, y):
        # Get the action with the highest Q-value for the current state (exploitation)
        state = (x, y)
        possible_actions = [action for action in range(4) if action in self.q_table.get(state, {})]
        if not possible_actions:
            # If no Q-values are available for the current state, explore (choose randomly)
            return random.choice([0, 1, 2, 3])
        return max(possible_actions, key=lambda a: self.q_table[state][a])

    def update_q_value(self, current_state, new_state):

        # Get the Q-value for the current state-action pair
        current_q = self.q_table.get(current_state, {}).get(self.action, 0)

        # Get the best Q-value for the new state (exploitation)
        best_action_new_state = self.get_best_action(*new_state)
        max_q_new_state = self.q_table.get(new_state, {}).get(best_action_new_state, 0)

        # Calculate the updated Q-value using the Q-learning formula
        updated_q = current_q + alpha * (self.maze.get_reward(*new_state) + gamma * max_q_new_state - current_q)

        # Update the Q-table with the new Q-value
        if current_state not in self.q_table:
            self.q_table[current_state] = {}
        self.q_table[current_state][self.action] = updated_q
    
    def get_q_table(self):
        return self.q_table
    
    def display_q_table(self):
        # Display the Q-table as a 2D grid
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                print("{:6.2f}".format(self.q_table.get((x, y), {}).get(0, 0)), end=" ")
            print()
        print()
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                print("{:6.2f}".format(self.q_table.get((x, y), {}).get(2, 0)), end=" ")
            print()
        print()
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                print("{:6.2f}".format(self.q_table.get((x, y), {}).get(1, 0)), end=" ")
            print()
        print()
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                print("{:6.2f}".format(self.q_table.get((x, y), {}).get(3, 0)), end=" ")
            print()
        print("--------------------------------------------------")
    
    # 
