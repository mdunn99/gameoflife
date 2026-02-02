import pygame
import math
import numpy as np
from time import sleep

# Initialize Pygame
pygame.init()

# set color of live cell
color = (255,255,255)

array = np.ones((16, 16), dtype=int) # placeholder for real array

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
    sleep(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # because the screen is resizable, we want to continuously get the
    # sizes so that we can fill the screen properly
    screen_width, screen_height = screen.get_size()

    # draw the array
    for row_i, row in enumerate(array):
        for cell_i, cell in enumerate(row):
            #print(f"cell: {cell} at position {row_i, cell_i}")
            if cell == 1:
                pygame.draw.rect(screen, color,
                                pygame.Rect(cell_i*cell_width,row_i*cell_height,cell_width,cell_height))
                
            '''if i % (square_width*2) == 0:

                print(f"drew rectangle at position {i}")
            else:
                continue'''
            pygame.display.flip()
            sleep(0.005)

    sleep(1)
    screen.fill((0,0,0))
    pygame.display.flip()
# Quit Pygame
pygame.quit()