from gui.game_interface import GameWindow
from maze.maze import Maze
import constants as c
from agent.agent import Agent
from agent.Q_agent import QAgent
import pygame


generator_algorithm = ["prim", "randomDFS"]

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
    Q_agent = QAgent(maze)
    game_window = GameWindow(maze, Q_agent)
    # lancer 3 gameloops en mesurant le temps d'execution de chaque gameloop et afficher les resultats
    tables = []
    game_window.game_loop(1)
    for i in range(3):
        game_window.game_loop(10000)
        print("Agent path length: ", len(Q_agent.agent_path))
        tables.append(Q_agent.q_table)

        # Process events before starting the next game loop
        pygame.event.pump()
        pygame.event.clear()

    # tester l'égalité des elements de la liste tables
    print(tables[0] == tables[1])   
    print(tables[1] == tables[2])
    print(tables[0] == tables[2])
    
    # Q_agent.agent_path = []
    # game_window.game_loop()
    # print("Agent path length: ", len(Q_agent.agent_path))
    # print agent path
    # print("Agent path: ", Q_agent.agent_path)
    

