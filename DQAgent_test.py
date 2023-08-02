from maze.maze import Maze
import constants as c
import numpy as np
from agent.DQ_agent import DQAgent


def train_agent(agent, num_episodes=1000, max_steps_per_episode=1000):
    for episode in range(1, num_episodes + 1):
        state = agent.get_state(agent.maze.matrix, agent.maze.exit)
        agent.state_size = len(state)
        total_reward = 0


        
        for step in range(max_steps_per_episode):
            # Take an action using the DQAgent's epsilon-greedy policy
            action = agent.act()

            # Perform the action in the environment
            next_state, reward, done = agent.step(action)


            # Store the experience in the replay buffer
            agent.remember(state, action, reward, next_state, done)
            
            
            # Move to the next state
            state = next_state

            # Accumulate the reward for this episode
            total_reward += reward

            if done:
                break


        # Perform experience replay to update the DQNetwork
        agent.replay()

        # Optionally, you can update the target network at some frequency
        if episode % agent.update_target_frequency == 0:
            agent.update_target_network()

        # Optionally, you can print the rewards per episode to monitor the training progress
        print(f"Episode {episode}/{num_episodes}, Total Reward: {total_reward}")


if __name__ == "__main__":

    maze = Maze(width= c.MAZE_WIDTH, height= c.MAZE_HEIGHT)
    print(maze.matrix)

    # Create the DQAgent
    dqn_agent = DQAgent(maze, action_size=4,
                        learning_rate=0.001, discount_factor=0.99, epsilon=1.0, epsilon_decay=0.995,
                        epsilon_min=0.01, batch_size=32, memory_size=1000)
    
    for i in range(100):
        state = dqn_agent.get_state(maze.matrix, maze.exit)
        a = dqn_agent.act()
        print(a)
        print("before", dqn_agent.position)
        dqn_agent.step(a)
        print("after", dqn_agent.position)
        next_state = dqn_agent.get_state(maze.matrix, maze.exit)
        print(np.array_equal(state, next_state))

        dqn_agent.remember(state, a, 0, next_state, False)

    # let's see what's inside memory
    for i in range(5):
        print(dqn_agent.memory[0][i])

    # debug the replay function
    dqn_agent.replay()