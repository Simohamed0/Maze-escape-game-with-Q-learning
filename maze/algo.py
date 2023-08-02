import random
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



def generate_random_maze_eller(self):
    # Step 1: Initialize the first row cells to each exist in their own set.
    sets = [{(x, 0)} for x in range(self.width)]

    # Step 2: Randomly join adjacent cells, but only if they are not in the same set.
    for y in range(1, self.height):
        for x in range(self.width):
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1)]
            valid_neighbors = [n for n in neighbors if self.is_within_maze(*n)]
            random.shuffle(valid_neighbors)

            if random.random() < 0.5:
                self.matrix[x, y] = MAZE_PATH
            
            else:    
                for neighbor_x, neighbor_y in valid_neighbors:
                    if (neighbor_x, neighbor_y) not in sets[x]:
                        sets[x].add((neighbor_x, neighbor_y))
                        sets[neighbor_x].add((neighbor_x, neighbor_y))
                        self.matrix[neighbor_x, neighbor_y] = MAZE_PATH
                        break

    # Step 3: For each set, randomly create vertical connections downward to the next row.
    for x in range(self.width):
        for y in range(1, self.height):
            if (x, y) in sets[x]:
                # Randomly choose a cell below to connect with
                valid_below_cells = [(nx, y + 1) for nx in range(self.width) if (nx, y + 1) not in sets[nx]]
                if valid_below_cells:
                    below_x, below_y = random.choice(valid_below_cells)
                    sets[x].add((below_x, below_y))
                    sets[below_x].add((below_x, below_y))
                    if below_x < self.width and below_y < self.height:
                        self.matrix[below_x, below_y] = MAZE_PATH  # Check if below_x and below_y are within range
                    break

    # Step 4: Flesh out the next row by putting any remaining cells into their own sets.
    for x in range(self.width):
        if (x, self.height - 1) not in sets[x]:
            sets[x].add((x, self.height - 1))
            self.matrix[x, self.height - 1] = MAZE_PATH

    # Step 5: Repeat until the last row is reached.
    for y in range(self.height - 2, 0, -1):
        for x in range(self.width):
            if (x, y) not in sets[x]:
                neighbors = [(x - 1, y), (x + 1, y), (x, y + 1)]
                valid_neighbors = [n for n in neighbors if self.is_within_maze(*n) and (x, y + 1) in sets[x]]
                if valid_neighbors:
                    neighbor_x, neighbor_y = random.choice(valid_neighbors)
                    sets[x].add((neighbor_x, neighbor_y))
                    sets[neighbor_x].add((neighbor_x, neighbor_y))
                    if neighbor_x < self.width:
                        self.matrix[neighbor_x, neighbor_y] = MAZE_PATH  # Check if neighbor_x is within range

    # Step 6: For the last row, join all adjacent cells that do not share a set.
    for x in range(self.width - 1):
        if (x, self.height - 1) not in sets[x]:
            right_x, right_y = x + 1, self.height - 1
            if (right_x, right_y) not in sets[right_x]:
                sets[x].add((right_x, right_y))
                sets[right_x].add((right_x, right_y))
                if right_x < self.width:
                    self.matrix[right_x, right_y] = MAZE_PATH

    self.matrix[self.start] = MAZE_START
    self.matrix[self.exit] = MAZE_EXIT




def generate_random_maze_hunt_and_kill(maze):
    width, height = maze.width, maze.height
    matrix = maze.matrix
    
    # Step 1: Choose a random starting location
    start_x, start_y = random.randint(0, width-1), random.randint(0, height-1)
    matrix[start_x, start_y] = MAZE_PATH
    
    # Step 2: Perform random walk until the exit point is reached
    current_x, current_y = start_x, start_y
    while (current_x, current_y) != maze.exit:
        # Get the list of possible neighbors to move
        possible_neighbors = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = current_x + dx, current_y + dy
            if 0 <= nx < width and 0 <= ny < height:
                possible_neighbors.append((nx, ny))
        
        # Choose a random neighbor to move to
        next_x, next_y = random.choice(possible_neighbors)
        matrix[next_x, next_y] = MAZE_PATH
        matrix[(current_x + next_x) // 2, (current_y + next_y) // 2] = MAZE_PATH  # Carve the passage
        current_x, current_y = next_x, next_y

    # Set the agent starting position and reset the agent path
    maze.start = start_x, start_y
    maze.agent_position = maze.start
    maze.agent_path = [maze.agent_position]

# Now, you can call the generate_random_maze function in the __init__ method of the Maze class like this:
# generate_random_maze(self)
