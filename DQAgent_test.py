from maze.maze import Maze
import constants as c
import numpy as np
from agent.DQ_agent import DQAgent


def train_agent(agent, num_episodes=1000, max_steps_per_episode=100):
    
    for episode in range(1, num_episodes + 1):
        
        # Reset the environment at the beginning of the episode
        agent.reset()
        state = agent.get_state(agent.maze.matrix, agent.maze.exit)
        agent.state_size = len(state)
        total_reward = 0
        
        for step in range(max_steps_per_episode):
            # Take an action using the DQAgent's epsilon-greedy policy
            action = agent.act(state)

            # Perform the action in the environment
            next_state, reward, done = agent.step(action)


            # Store the experience in the replay buffer
            agent.remember(state, action, reward, next_state, done)
            
            
            # Move to the next state
            state = next_state

            # Accumulate the reward for this episode
            total_reward += reward

            print(f"Step {step + 1}/{max_steps_per_episode}, Total Reward: {total_reward}")
            if done:
                break

        
       
        # Perform experience replay to update the DQNetwork
        agent.replay()

        # Optionally, you can update the target network at some frequency
        if episode % 5 == 0:
            agent._soft_update_target_network()

        # Optionally, you can print the rewards per episode to monitor the training progress
        print(f"Episode {episode}/{num_episodes}, Total Reward: {total_reward}")

    
    
    # Save the DQNetwork in model_weights.h5
    agent.model.save_weights("model_weights.h5")


# test 

if __name__ == "__main__":

    maze = Maze(width= c.MAZE_WIDTH, height= c.MAZE_HEIGHT)
    print(maze.matrix)

    # Create the DQAgent
    dqn_agent = DQAgent(maze, action_size=4,
                        learning_rate=0.001, discount_factor=0.99, epsilon=0.1, epsilon_decay=0.995,
                        epsilon_min=0.01, batch_size=32, memory_size=1000)


    train_agent(dqn_agent, num_episodes=10, max_steps_per_episode=100)

    # use the saved model and gui to test the agent
    


    