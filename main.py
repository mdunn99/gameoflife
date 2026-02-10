import pygame
from pygame.locals import *
import math
import numpy as np
from time import sleep

# Initialize Pygame
pygame.init()

# set color of live cell
white = (255,255,255)
black = (0, 0, 0)
red = (255,0,0)

array_0 = np.zeros((16, 16), dtype=int) # initialize empty array for initial array

# counts the live cells surrounding a cell
def count_live_cells(row, column):
    # get around python negative indices
    # if the row value is the minimum or maximum, 
    # assume that the outer cells are dead
    live_cells = 0
    try:
        live_cells += array_0[row-1][column] if row != 0 else 0                 # up
        live_cells += array_0[row-1][column+1] if row != 0 else 0               # up right
        live_cells += array_0[row][column+1] # will get caught by error         # right
        live_cells += array_0[row+1][column+1] if row != len(array_0)-1 else 0  # down right
        live_cells += array_0[row+1][column] if row != len(array_0)-1 else 0    # down
        live_cells += array_0[row+1][column-1] if row != len(array_0)-1 else 0  # down left
        live_cells += array_0[row][column-1] # will get caught by error     # left
        live_cells += array_0[row-1][column-1]                              # up left
    except (ValueError,IndexError):
        pass # do not append
    return live_cells

def determine_dead_cell_status(live_cell_count):
    dead_cell_status = 1 if live_cell_count == 3 else 0
    return dead_cell_status

def determine_live_cell_status(live_cell_count):
    if live_cell_count < 2 or live_cell_count > 3:
        live_cell_status = 0 # dies
    elif live_cell_count == 2 or live_cell_count == 3:
        live_cell_status = 1
    return live_cell_status

def determine_new_cell_status(row, column, cell):
    live_cell_count = count_live_cells(row, column)
    if cell == 0: # cell is dead
        cell_status = determine_dead_cell_status(live_cell_count)
    else: # cell is live
        cell_status = determine_live_cell_status(live_cell_count)
    #print(live_cell_count)
    return cell_status

def simulation_loop():
    array_n = np.zeros((16, 16), dtype=int) # re-initialize array_n as empty every time simulation is run
    for row_index, row in enumerate(array_0):
        for column_index, cell_0 in enumerate(row):
            cell_n = determine_new_cell_status(row_index, column_index, cell_0) # define a new cell for the array of the next generation
            array_n[row_index][column_index] = cell_n # append this new cell to its corresponding location in the new array (array_n)
    return array_n

# superimposing the array onto the screen
array_width_height = math.sqrt(array_0.size)
arr_size = arr_width, arr_height = array_width_height, array_width_height
screen_size = screen_width, screen_height = 720, 720
cell_size = cell_width, cell_height = screen_width/arr_width, screen_height/arr_height
buffer_px = 2 # there needs to be an appropriate formula for this

# calculate real array position based on pixel pos
# we use floor division to divide the pixel pos by the width/height (same) of the cell
def get_array_index(pos):
    row = int(pos[1] // cell_width)
    cell = int(pos[0] // cell_width)
    array_index = (row, cell) # placeholder
    return array_index

# update array value associated with position clicked
def update_array(pos):
    print(f"\nmouse clicked at position: {pos}")
    array_index = get_array_index(pos)
    row = array_index[0]
    cell = array_index[1]
    print(f"cell at pos {pos} detected as row {row}, cell {cell} with value: {array_0[row][cell]}")
    # if cell is off, turn it on
    # vice versa
    # THIS FUNCTIONALITY WILL HAVE TO BE EDITED WHEN THE SIMULATION ACTUALLY BEGINS
    if array_0[row][cell] == 0:
        array_0[row][cell] = 1
    else:
        array_0[row][cell] = 0
    print(f"cell {cell} at row {row} is now: {array_0[row][cell]}")
    return

# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game of Life")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left-click
                pos = pygame.mouse.get_pos()
                update_array(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                print("starting simulation")
                array_0 = simulation_loop() # define the initial, main array as the new array returned by the processing of the rules

    # draw the grid
    for row_i, row in enumerate(array_0):
        for cell_i, cell in enumerate(row):
            pygame.draw.rect(screen, (255,255,255),
                             pygame.Rect(cell_i*cell_width,row_i*cell_height,1,cell_height))
            pygame.draw.rect(screen, (255,255,255),
                             pygame.Rect(cell_i*cell_width,row_i*cell_height,cell_width,1))

    # draw the array
    for row_i, row in enumerate(array_0):
        for cell_i, cell in enumerate(row):
            # if the cell is active, draw it as such!
            if cell == 1:
                # making the size of the cells "*0.90" makes the cells slightly smaller than the
                # size of the whole cell, allowing the grid lines to be visible.
                # we have to adjust the position accordingly, so we add a buffer buffer_px to each coordinate for the cells
                pygame.draw.rect(screen, white,
                                pygame.Rect((cell_i*cell_width)+buffer_px,(row_i*cell_height)+buffer_px,cell_width*0.90,cell_height*0.90))
            else:
                pygame.draw.rect(screen, black,
                                pygame.Rect((cell_i*cell_width)+buffer_px,(row_i*cell_height)+buffer_px,cell_width*0.90,cell_height*0.90))

    pygame.display.flip()
# Quit Pygame
pygame.quit()