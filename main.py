from gui.game_interface import GameWindow
from maze.maze import Maze
import constants as c


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
    game_window = GameWindow(maze)
    game_window.game_loop()
