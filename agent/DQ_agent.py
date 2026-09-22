import numpy as np
import random
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
                 epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, batch_size=32, memory_size=1000, tau=0.1):
        
        super().__init__(maze)
        self.state_size = maze.width * maze.height + 2 + len(maze.flags)
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.tau = tau
        self.memory = deque(maxlen=memory_size)

        # Build the Deep Q-Network
        self.model = self._build_model()
        self.target_model = self._build_model()
        self._soft_update_target_network()

    

    def reset(self):
        super().reset()

    def _build_model(self):
        
        # the input is the state size
        model = Sequential()
        model.add(Dense(64, input_shape=(self.state_size,), activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    # remember(state, action, reward, next_state, done) function
    def remember(self, state, action, reward, next_state, done):
        # Add the experience to agent's memory
        self.memory.append((state, action, reward, next_state, done))
        

    
    def get_state(self, maze_matrix=None, goal_position=None):
        flags = [float(flag in self.maze.flags_collected) for flag in self.maze.flags]
        return np.concatenate((np.asarray(self.agent_position, dtype=float), self.maze.matrix.flatten(), flags))


    def act(self,state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        # reshape the state to (1, state_size)
        state = np.reshape(state, [1, self.state_size])
        q_values = self.model.predict(state, verbose=0)
        action = np.argmax(q_values[0])
        print("action not random: {}".format(action))
        return action
    

    def step(self, action):
        self.agent_position, reward, done = self.maze.step(self.agent_position, action)
        self.agent_path.append(self.agent_position)
        next_state = self.get_state()
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
        target_q_values = self.model.predict(states, verbose=0)
        next_q_values_target = self.target_model.predict(next_states, verbose=0)
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

    def load_saved_model(self, path):
        self.model.load_weights(path)
        self.target_model.load_weights(path)
