import pygame
from pygame.locals import QUIT

class GameWindow:
    def __init__(self, maze):
        self.maze = maze
        self.cell_size = 30
        self.width = maze.width * self.cell_size
        self.height = maze.height * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Maze Escape")
        self.colors = {
            "wall": (0, 0, 0),
            "path": (255, 255, 255),
            "start": (0, 255, 0),
            "exit": (255, 0, 0),
            "agent": (0, 0, 255)
        }

    def draw_maze(self):
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                cell = self.maze.maze[x, y]
                color = self.colors["wall"] if cell == 1 else self.colors["path"]
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                if (x, y) == self.maze.start:
                    pygame.draw.rect(self.screen, self.colors["start"], (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif (x, y) == self.maze.exit:
                    pygame.draw.rect(self.screen, self.colors["exit"], (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def draw_agent(self, x, y):
        pygame.draw.rect(self.screen, self.colors["agent"], (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def update_display(self, agent_position):
        self.screen.fill((255, 255, 255))
        self.draw_maze()
        self.draw_agent(agent_position[0], agent_position[1])
        pygame.display.update()
        self.clock.tick(60)

    def game_loop(self):
        pygame.init()
        #agent = Agent(...)  # Initialize your agent here
        x, y = self.maze.start
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

            #action = agent.get_action(x, y)
            action = 0  # Replace this with your agent's action
            next_x, next_y = x, y

            if action == 0:  # Up
                next_x -= 1
            elif action == 1:  # Down
                next_x += 1
            elif action == 2:  # Left
                next_y -= 1
            else:  # Right
                next_y += 1

            if self.maze.is_within_maze(next_x, next_y) and not self.maze.is_wall(next_x, next_y):
                x, y = next_x, next_y
                self.update_display((x, y))


