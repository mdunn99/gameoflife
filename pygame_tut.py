import pygame
import math
import numpy as np
from time import sleep

# Initialize Pygame
pygame.init()

# set color of live cell
color = (255,255,255)

array = np.zeros((16, 16), dtype=int) # placeholder for real array

array_width_height = math.sqrt(array.size)

# size of the array
arr_size = arr_width, arr_height = array_width_height, array_width_height
screen_size = screen_width, screen_height = 512, 512
cell_size = cell_width, cell_height = screen_width/arr_width, screen_height/arr_height

# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game of Life")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the grid
    for row_i, row in enumerate(array):
        for cell_i, cell in enumerate(row):
            pygame.draw.rect(screen, (255,255,255),
                             pygame.Rect(cell_i*cell_width,row_i*cell_height,1,cell_height))
            pygame.draw.rect(screen, (255,255,255),
                             pygame.Rect(cell_i*cell_width,row_i*cell_height,cell_width,1))
            pygame.display.flip()
    # draw the array
    for row_i, row in enumerate(array):
        for cell_i, cell in enumerate(row):
            # if the cell is active, draw it as such!
            if cell == 1:
                # making the size of the cells "*0.99" makes the cells slightly smaller than the
                # proper size of the whole cell, allowing the grid lines to be visible
                pygame.draw.rect(screen, color,
                                pygame.Rect(cell_i*cell_width,row_i*cell_height,cell_width*0.99,cell_height*0.99))
            pygame.display.flip()
            sleep(0.005)

    pygame.display.flip()
# Quit Pygame
pygame.quit()