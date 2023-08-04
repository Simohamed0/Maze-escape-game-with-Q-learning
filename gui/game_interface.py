import pygame
from pygame.locals import QUIT
import time

class GameWindow:
    def __init__(self, maze, agent):
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
        self.agent_image = pygame.image.load("assets/arrow.png")  
        self.agent_image = pygame.transform.scale(self.agent_image, (self.cell_size, self.cell_size))
        self.agent = agent
        self.teleport_image = pygame.image.load("assets/teleport.jpeg")
        self.teleport_image = pygame.transform.scale(self.teleport_image, (self.cell_size, self.cell_size))




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

        # Calculate the angle of rotation based on the direction of movement but switching roght and left
        if dx == 1 and dy == 0:
            angle = 180
        elif dx == -1 and dy == 0:
            angle = 0
        elif dx == 0 and dy == 1:
            angle = 90
        else:
            angle = 270       


        # Rotate the agent image to the calculated angle
        rotated_agent_image = pygame.transform.rotate(self.agent_image, angle)

        # Draw the rotated agent image on the game window at the current position
        self.screen.blit(rotated_agent_image, (x * self.cell_size, y * self.cell_size))

    def draw_flags(self):
        for flag_pos in self.maze.flags:
            if flag_pos in self.maze.flags_collected:
                flag_color = (128, 128, 0)  
            else:
                flag_color = (255, 255, 0)  

            flag_rect = pygame.Rect(flag_pos[0] * self.cell_size, flag_pos[1] * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, flag_color, flag_rect)

    def draw_teleport(self):
        for teleport_point in self.maze.teleport_points:
            teleport_rect = pygame.Rect(teleport_point[0] * self.cell_size, teleport_point[1] * self.cell_size, self.cell_size, self.cell_size)
            self.screen.blit(self.teleport_image, teleport_rect)


    def update_display(self):
        self.screen.fill((255, 255, 255))
        self.draw_maze()
    
        # Get the agent's current and next positions
        agent_x, agent_y = self.agent.get_position()
        next_agent_x, next_agent_y = self.agent.get_next_position()  
        # Draw the agent at its current and next positions
        self.draw_agent(agent_x, agent_y, next_agent_x, next_agent_y)
        # Draw the flags
        self.draw_flags()
        # Draw the teleportation points
        self.draw_teleport()
        pygame.display.update()
        self.clock.tick(60)


    def game_loop(self, delta):
        pygame.init()
        start_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                
            if self.maze.is_exit(*self.agent.get_position()) and len(self.maze.flags_collected) == len(self.maze.flags):
                print("You escaped!")
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Time taken for the simulation:", elapsed_time)
                self.agent.time_list.append(elapsed_time)
                # pygame.quit()
                # Reset the flags_collected list to make all flags uncollected again
                self.maze.flags_collected = []
                # Reset the visited_states set to allow revisiting states in the next game
                self.maze.visited_states.clear()
                # Reset the agent's position to the start position
                self.agent.set_position(*self.maze.start)
                return
            
            teleport_position = self.maze.is_teleport(*self.agent.get_position())

            if teleport_position:
                destination = self.get_teleport_destination(teleport_position)
                self.agent.set_position(*destination)  # Set the agent's position to the destination

            # Move the agent in the maze 
            self.agent.move()
            # self.agent.display_q_table()
            self.check_flags()

            self.update_display()

            # Add a delay of 500 milliseconds (0.5 seconds) between each movement
            pygame.time.delay(delta)

    def check_flags(self):
        # Check if the agent has landed on a flag position
        agent_pos = self.agent.get_position()
        for flag in self.maze.flags:
            if agent_pos == flag and flag not in self.maze.flags_collected:
                self.maze.flags_collected.append(flag)



    def get_teleport_destination(self, teleport_position):
        # Get the destination of the teleportation point
        for i, teleport_point in enumerate(self.maze.teleport_points):
            if teleport_position == teleport_point:
                destination = self.maze.teleport_points[1 - i]
                return destination

            

