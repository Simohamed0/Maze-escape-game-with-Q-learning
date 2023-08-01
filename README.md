<!-- Project Title -->
# Maze Escape Game with Q-Learning

<!-- Project Description -->
Escape the maze with the help of a Q-learning agent! This is a Python project that implements Q-learning to solve mazes. The agent explores the maze and learns to find the optimal path from the starting point to the exit.

<!-- Badges (Optional) -->
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

<!-- Table of Contents -->
## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How it Works](#how-it-works)
- [Demo](#demo)
- [Contributing](#contributing)
- [Authors](#authors)

<!-- Introduction -->
## Introduction


<!-- Features -->
## Features
List the key features of your project:
- Random maze generation
- Q-learning agent implementation
- Maze visualization with Pygame

- ...

<!-- Installation -->
## Installation
Provide instructions on how to install and set up your project. You can include code blocks to show commands.
```bash
pip install -r requirements.txt
python main.py
```



<!-- Authors -->
## Authors

This project was developed by:

- Mohamed FAID ([GitHub](https://github.com/Simohamed0))
- Youssef FAID ([GitHub](https://github.com/FaidYoussef))


<!-- what does the agent learn by time? -->

As the agent interacts with the environment and moves through the maze, it learns to improve its behavior and navigation strategy through the Q-learning algorithm. The Q-learning algorithm allows the agent to learn by updating its Q-table based on the rewards it receives after taking specific actions in different states.

Here's how the agent learns over time:

1. **Exploration vs. Exploitation**: Initially, the agent starts with little to no knowledge about the maze and its environment. It explores the maze by randomly choosing actions with a certain exploration rate (epsilon) to discover new paths and states.

2. **Updating Q-values**: During exploration, the agent takes actions based on the epsilon-greedy policy, and it observes the resulting rewards for each state-action pair. The Q-learning algorithm updates the Q-values in the Q-table based on the observed rewards and the best possible action in the next state.

3. **Reinforcement**: The agent receives positive or negative rewards based on its actions. Positive rewards are given when the agent moves closer to the goal, and negative rewards (or punishments) are given when the agent hits a wall or takes a suboptimal path. The agent learns to associate higher Q-values with actions that lead to more rewards over time.

4. **Exploitation of Q-table**: As the agent accumulates experience through exploration and learning, it starts to exploit the learned knowledge by choosing actions with the highest Q-values for each state. The more the agent explores, the more it learns about the optimal path to reach the goal.

5. **Convergence to Optimal Policy**: With sufficient exploration and learning iterations, the Q-values in the Q-table converge to their optimal values. The agent gradually develops a policy that allows it to navigate the maze efficiently, choosing the best actions to reach the goal while avoiding obstacles.

6. **Optimal Path**: Once the Q-values have converged, the agent should be able to follow the optimal path from the starting position to the goal position with a high degree of success.

It's important to note that the learning process is influenced by the learning rate (alpha) and the discount factor (gamma). The learning rate determines how much the agent should value new information over past experiences, while the discount factor balances the importance of immediate rewards versus future rewards.

The learning process is not always deterministic, and the agent might need to explore and learn from various paths to discover the optimal strategy. Over time, with enough training iterations, the agent should become proficient in navigating the maze and finding the shortest path to the goal.