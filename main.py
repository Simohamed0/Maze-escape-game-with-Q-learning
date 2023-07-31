from gui.game_interface import GameWindow
from maze.maze import Maze

if __name__ == "__main__":
    maze = Maze(width=10, height=10)  # Customize maze size as needed
    game_window = GameWindow(maze)
    game_window.game_loop()