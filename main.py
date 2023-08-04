from gui.game_interface import GameWindow
from maze.maze import Maze
import constants as c
from agent.agent import Agent
from agent.Q_agent import QAgent
from agent.DoubleQAgent import DoubleQAgent
import pygame


generator_algorithm = ["prim", "eller", "hunt-and-kill"]

# argument parser for command line arguments and what algorithm to use
def parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", help="choose which algorithm to use to generate maze", choices=generator_algorithm, default="prim")
    args = parser.parse_args()
    return args.algorithm

if __name__ == "__main__":

    algorithm = parser()
    maze = Maze(width=c.MAZE_WIDTH, height= c.MAZE_HEIGHT, generator_algorithm=algorithm)
    print(maze.matrix)
    agent = DoubleQAgent(maze)
    game_window = GameWindow(maze, agent)
    # lancer 3 gameloops en mesurant le temps d'execution de chaque gameloop et afficher les resultats
    lenghts = []
    for i in range(100):
        # initialiser la position de l'agent à la position de départ
        agent.agent_position = maze.start
        game_window.game_loop(1)
        print("Agent path length: ", len(agent.agent_path))
        lenghts.append(len(agent.agent_path))
        print("episode ", i+1,"take", len(agent.agent_path), "steps")
        
    pygame.quit()
    # remove the first element of the list
    agent.time_list.pop(0)
    # plot time list of agent in a big figure
    import matplotlib.pyplot as plt
    plt.figure(figsize=(20,20))
    plt.plot(agent.time_list)
    plt.xlabel("episode")
    plt.ylabel("time")
    plt.title("time taken for each episode")
    plt.show()

    for i in range(len(lenghts)):
        if i > 0:
            lenghts[i] -= lenghts[i-1]
    

    # plot lenghts list of agent in a big figure
    plt.figure(figsize=(20,20))
    plt.plot(lenghts)
    plt.xlabel("episode")
    plt.ylabel("length")
    plt.title("length of path taken for each episode")
    plt.show()


    
    # Q_agent.agent_path = []
    # game_window.game_loop()
    # print("Agent path length: ", len(Q_agent.agent_path))
    # print agent path
    # print("Agent path: ", Q_agent.agent_path)
    

