import numpy as np
import random
import matplotlib.pyplot as plt
from collections import deque
from agent.agent import Agent
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # '2' means to only display error messages

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam


# actions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3



class DQAgent(Agent):
    def __init__(self, maze, action_size=4, learning_rate=0.001, discount_factor=0.99,
                 epsilon=0, epsilon_decay=0.995, epsilon_min=0.01, batch_size=32, memory_size=1000, tau=0.1):
        
        super().__init__(maze)
        self.state_size = maze.width * maze.height + 5
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.tau = tau
        self.memory = deque(maxlen=memory_size)
        self.model_weights_path = 'model_weights.h5'

        # Build the Deep Q-Network
        self.model = self._build_model()
        self.target_model = self._build_model()
        self._soft_update_target_network()

    

    def reset(self):
        self.position = self.maze.start

    def _build_model(self):
        
        # the input is the state size
        model = Sequential()
        model.add(Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    # remember(state, action, reward, next_state, done) function
    def remember(self, state, action, reward, next_state, done):
        # Add the experience to agent's memory
        self.memory.append((state, action, reward, next_state, done))
        

    
    def get_state(self,maze_matrix, goal_position):
        state = []

        # Add agent's x and y coordinates to the state
        state.extend(self.position)

        # Flatten the maze matrix and add it to the state
        for row in maze_matrix:
            state.extend(row)

        # Add goal's x and y coordinates to the state
        state.extend(goal_position)

        # Calculate and add the Manhattan distance from the agent to the goal
        distance_to_goal = abs(self.position[0] - goal_position[0]) + abs(self.position[1] - goal_position[1])
        state.append(distance_to_goal)

        return state


    def act(self,state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        # reshape the state to (1, state_size)
        state = np.reshape(state, [1, self.state_size])
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])
    

    def step(self, action):
        # Perform the given action in the environment (maze)

        # Update the agent's position based on the chosen action
        if action == UP:
            next_position = (self.position[0] - 1, self.position[1])
        elif action == DOWN:
            next_position = (self.position[0] + 1, self.position[1])
        elif action == LEFT:
            next_position = (self.position[0], self.position[1] - 1)
        elif action == RIGHT:
            next_position = (self.position[0], self.position[1] + 1)
        
        reward = 0
        # Check if the next position is within the maze boundaries
        if next_position[0] >= 0 and next_position[0] < self.maze.height and next_position[1] >= 0 and next_position[1] < self.maze.width:
            if self.maze.matrix[next_position[0]][next_position[1]] == 0:
                self.position = next_position
            else:
                reward = -1

        # Get the state representation at the new position
        next_state = self.get_state(self.maze.matrix, self.maze.exit)

        # Check if the agent has reached the goal position
        done = self.position == self.maze.exit

        # Assign a reward based on the agent's new position
        if done:
            reward = 50
            
        return next_state, reward, done

    def replay(self):
        # Check if the replay buffer has enough experiences to sample a batch
        if len(self.memory) < self.batch_size:
            return    

        # Sample a batch of experiences from the replay buffer
        minibatch = random.sample(self.memory, self.batch_size)

        # Convert the elements of minibatch into separate lists
        states, actions, rewards, next_states, dones = [], [], [], [], []
        for experience in minibatch:
            state, action, reward, next_state, done = experience
            states.append(np.array(state))
            actions.append(np.array(action))
            rewards.append(reward)
            next_states.append(np.array(next_state))
            dones.append(done)

        # Convert the lists to NumPy arrays
        states = np.array(states)
        actions = np.array(actions)
        rewards = np.array(rewards)
        next_states = np.array(next_states)
        dones = np.array(dones)

        print("states shape: {}".format(states.shape))

        # Calculate the target Q-values using the target network
        target_q_values = self.model.predict(states)
        next_q_values_target = self.target_model.predict(next_states)
        max_next_q_values = np.max(next_q_values_target, axis=1)

        # Calculate the target Q-values based on the Bellman equation
        targets = rewards + (1 - dones) * self.discount_factor * max_next_q_values

        # Update the Q-values for the chosen actions
        target_q_values[np.arange(self.batch_size), actions] = targets

        # Train the DQN with the current batch of experiences
        loss = self.model.train_on_batch(states, target_q_values)

        # Optionally, you can log and plot the loss 
        print("loss: {}".format(loss))




    def _soft_update_target_network(self):
        model_weights = self.model.get_weights()
        target_model_weights = self.target_model.get_weights()
        for idx in range(len(model_weights)):
            target_model_weights[idx] = (1 - self.tau) * target_model_weights[idx] + self.tau * model_weights[idx]
        self.target_model.set_weights(target_model_weights)

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self):
        self.model.load_weights(self.model_weights_path)

