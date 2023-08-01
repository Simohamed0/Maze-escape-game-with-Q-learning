import numpy as np
import random
# collections of algorithms to generate mazes ;)

MAZE_WALL = 1
MAZE_PATH = 0
MAZE_START = 3
MAZE_EXIT = 4

# function to generate random maze using Prim's algorithm
def generate_random_maze_prim(maze):
        visited = np.full((maze.width, maze.height), False)
        walls = []
        
        def add_walls(x, y):
            if x > 0 and not visited[x - 1, y]:
                walls.append((x - 1, y))
            if x < maze.width - 1 and not visited[x + 1, y]:
                walls.append((x + 1, y))
            if y > 0 and not visited[x, y - 1]:
                walls.append((x, y - 1))
            if y < maze.height - 1 and not visited[x, y + 1]:
                walls.append((x, y + 1))
        
        def mark_visited(x, y):
            visited[x, y] = True
            add_walls(x, y)
        
        start_x, start_y = maze.start
        mark_visited(start_x, start_y)
        
        while walls:
            x, y = walls.pop(random.randint(0, len(walls) - 1))
            
            neighbors = []
            if x > 0 and visited[x - 1, y]:
                neighbors.append((x - 1, y))
            if x < maze.width - 1 and visited[x + 1, y]:
                neighbors.append((x + 1, y))
            if y > 0 and visited[x, y - 1]:
                neighbors.append((x, y - 1))
            if y < maze.height - 1 and visited[x, y + 1]:
                neighbors.append((x, y + 1))
            
            if len(neighbors) == 1:
                maze.matrix[x, y] = MAZE_PATH
                mark_visited(x, y)
        
        # Set start and exit positions
        maze.matrix[start_x, start_y] = MAZE_PATH
        exit_x, exit_y = maze.exit
        maze.matrix[exit_x, exit_y] = MAZE_PATH


