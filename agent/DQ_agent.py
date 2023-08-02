import numpy as np
import random
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam



class DQAgent:
    def __init__(self, maze, action_size=4, learning_rate=0.001, discount_factor=0.99,
                 epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, batch_size=32, memory_size=1000):
        
        self.state_size = maze.width * maze.height
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.memory = deque(maxlen=memory_size)

        # Build the Deep Q-Network
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()

        # Add input layer with state_size neurons and use ReLU activation
        model.add(Dense(32, input_dim=self.state_size, activation='relu'))

        # Add hidden layers
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))

        # Add output layer with action_size neurons (one for each action)
        model.add(Dense(self.action_size, activation='linear'))

        # Compile the model using Mean Squared Error as the loss function and Adam optimizer
        model.compile(loss='mean_squared_error', optimizer='adam')

        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        return np.argmax(self.model.predict(state)[0])

    def replay(self):
        # Check if the replay buffer has enough experiences to sample a batch
        if len(self.memory) < self.batch_size:
            return

        # Sample a batch of experiences from the replay buffer
        minibatch = np.array(random.sample(self.memory, self.batch_size))

        # Extract the individual components of the experiences
        states = np.vstack(minibatch[:, 0])
        actions = np.array(minibatch[:, 1], dtype=int)
        rewards = np.array(minibatch[:, 2])
        next_states = np.vstack(minibatch[:, 3])
        dones = np.array(minibatch[:, 4], dtype=bool)

        # Calculate the target Q-values using the target network
        target_q_values = self.model.predict(states)
        next_q_values_target = self.target_model.predict(next_states)
        max_next_q_values = np.max(next_q_values_target, axis=1)

        # Calculate the target Q-values based on the Bellman equation
        targets = rewards + (1 - dones) * self.discount_factor * max_next_q_values

        # Update the Q-values for the chosen actions
        for idx, action in enumerate(actions):
            target_q_values[idx][action] = targets[idx]

        # Train the DQN with the current batch of experiences
        loss = self.model.train_on_batch(states, target_q_values)

        # Optionally, you can log the loss or other metrics for monitoring the training process
        print("Loss: {}".format(loss))

        # Soft update the target network by updating its weights with the current model's weights
        self._soft_update_target_network()

    def _soft_update_target_network(self):
        model_weights = self.model.get_weights()
        target_model_weights = self.target_model.get_weights()
        for idx in range(len(model_weights)):
            target_model_weights[idx] = (1 - self.tau) * target_model_weights[idx] + self.tau * model_weights[idx]
        self.target_model.set_weights(target_model_weights)

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

