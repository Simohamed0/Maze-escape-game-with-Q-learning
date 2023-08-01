from gui.game_interface import GameWindow
from maze.maze import Maze
import constants as c


generator_algorithm = ["prim", "randomDFS"]

# argument parser
def parser():
    pass

if __name__ == "__main__":
    
    maze = Maze(c.MAZE_WIDTH, c.MAZE_HEIGHT)
    print(maze.matrix)
    game_window = GameWindow(maze)
    game_window.game_loop()
