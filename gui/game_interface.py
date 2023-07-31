import pygame
from pygame.locals import QUIT
from agent.dumb_agent import DumbAgent
import math

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
        # Load the image for the agent and resize it to the cell size
        self.agent_image = pygame.image.load("/home/youssef/Téléchargements/arrow.png")  # Replace "agent.png" with the actual path to your agent's image
        self.agent_image = pygame.transform.scale(self.agent_image, (self.cell_size, self.cell_size))


    def draw_maze(self):
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                cell = self.maze.matrix[x][y]
                color = self.colors["wall"] if cell == 1 else self.colors["path"]
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                if (x, y) == self.maze.start:
                    pygame.draw.rect(self.screen, self.colors["start"], (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif (x, y) == self.maze.exit:
                    pygame.draw.rect(self.screen, self.colors["exit"], (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def draw_agent(self, x, y, next_x, next_y):
        # Calculate the direction the agent is about to move
        dx, dy = next_x - x, next_y - y

        # Calculate the angle of rotation based on the direction of movement
        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)

        # Convert the angle to the range [0, 360] degrees
        angle_degrees %= 360

        # Rotate the agent image to the calculated angle
        rotated_agent_image = pygame.transform.rotate(self.agent_image, angle_degrees)

        # Draw the rotated agent image on the game window at the current position
        self.screen.blit(rotated_agent_image, (x * self.cell_size, y * self.cell_size))

    def update_display(self, agent_position, next_agent_position):
        self.screen.fill((255, 255, 255))
        self.draw_maze()
        self.draw_agent(agent_position[0], agent_position[1], next_agent_position[0], next_agent_position[1])
        pygame.display.update()
        self.clock.tick(60)

    def game_loop(self):
        pygame.init()
        agent = DumbAgent(self.maze)
        x, y = self.maze.start
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

            action = agent.get_action(x, y)
            next_x, next_y = x, y

            if action == 0:  # Up
                next_x -= 1
            elif action == 1:  # Down
                next_x += 1
            elif action == 2:  # Left
                next_y -= 1
            else:  # Right
                next_y += 1

            self.update_display((x, y), (next_x, next_y))
            if self.maze.is_within_maze(next_x, next_y) and not self.maze.is_wall(next_x, next_y):
                x, y = next_x, next_y

            if self.maze.is_exit(x, y):
                print("You escaped!")
                pygame.quit()
                return
            
            # Add a delay of 500 milliseconds (0.5 seconds) between each movement
            pygame.time.delay(1000)


