import argparse
import random

import numpy as np

import constants as c
from agent.DoubleQAgent import DoubleQAgent
from maze.maze import Maze


def parse_args():
    parser = argparse.ArgumentParser(description="Train a Double Q-learning maze agent")
    parser.add_argument("-a", "--algorithm", choices=("prim", "eller", "hunt-and-kill"), default="prim")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--plot", action="store_true")
    return parser.parse_args()


def train(agent, episodes, max_steps):
    lengths, solved = [], []
    for _ in range(episodes):
        agent.reset()
        success = False
        for _ in range(max_steps):
            if agent.move():
                success = True
                break
        lengths.append(len(agent.agent_path) - 1)
        solved.append(success)
    return lengths, solved


def main():
    args = parse_args()
    if args.episodes < 1 or args.max_steps < 1:
        raise ValueError("episodes and max-steps must be positive")
    random.seed(args.seed)
    np.random.seed(args.seed)
    maze = Maze(c.MAZE_WIDTH, c.MAZE_HEIGHT, args.algorithm)
    agent = DoubleQAgent(maze)
    lengths, solved = train(agent, args.episodes, args.max_steps)
    print(f"Solved {sum(solved)}/{args.episodes} episodes")
    if any(solved):
        successful_lengths = [length for length, success in zip(lengths, solved) if success]
        print(f"Mean successful path length: {np.mean(successful_lengths):.1f}")

    if args.render:
        from gui.game_interface import GameWindow
        import pygame

        agent.epsilon = 0.0
        agent.reset()
        GameWindow(maze, agent).game_loop(args.max_steps)
        pygame.quit()

    if args.plot:
        import matplotlib.pyplot as plt

        plt.plot(lengths)
        plt.xlabel("Episode")
        plt.ylabel("Steps")
        plt.title("Training episode length")
        plt.show()


if __name__ == "__main__":
    main()
