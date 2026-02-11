import pygame
from pygame.locals import *
import numpy as np
from time import sleep

# Initialize Pygame
pygame.init()

# set some RGB colors
white = (255,255,255)
black = (0, 0, 0)
red = (255,0,0)

array_width, array_height = (16,16) # configure the size of an array
screen_width, screen_height = 720, 720 # configure the size of the screen
array_0 = np.zeros((array_width, array_height), dtype=int) # initialize initial array as empty

# superimposing the array onto the screen
cell_width, cell_height = screen_width/array_width, screen_height/array_height

# in order for the cells not to cover the grid lines, they must be smaller
# than the full size of a cell on the superimposed array.
# so, cells are multipled by a value 0<x<1.

# however, they will still be painted in "the top left" of the position
# of the cell at array[n][n].

# buffer_px defines a "buffer" where the position of the cell,
# to be painted on the pygame display, is added to said buffer
# to attempt to center the cell.
buffer_px = 2

# calculate real array position based on pixel position.
#  use floor division to divide the pixel position by the width/height of the cell.
def get_array_indices(pos):
    row = int(pos[1] // cell_height)
    cell = int(pos[0] // cell_width)
    array_index = (row, cell)
    return array_index

# update array value associated with position clicked
def update_array_from_user_input(array_to_update, pos):
    array = np.copy(array_to_update)
    print(f"\nmouse clicked at position: {pos}")
    array_index = get_array_indices(pos)
    row = array_index[0]
    cell = array_index[1]
    print(f"cell at pos {pos} detected as row {row}, cell {cell} with value: {array_to_update[row][cell]}")
    # if cell is off, turn it on
    # vice versa
    if array_to_update[row][cell] == 0:
        array[row][cell] = 1
    else:
        array[row][cell] = 0
    print(f"cell {cell} at row {row} is now: {array[row][cell]}")
    return array

def draw_grid(array):
    for row_i, row in enumerate(array):
        for cell_i, cell in enumerate(row):
            pygame.draw.rect(screen, (255,255,255),
                             pygame.Rect(cell_i*cell_width,row_i*cell_height,1,cell_height))
            pygame.draw.rect(screen, (255,255,255),
                             pygame.Rect(cell_i*cell_width,row_i*cell_height,cell_width,1))
    return pygame.display.flip()

def draw_array(array):
    for row_i, row in enumerate(array):
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
    return pygame.display.flip()

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
        live_cells += array_0[row][column-1] # will get caught by error         # left
        live_cells += array_0[row-1][column-1]                                  # up left
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

def return_new_array(array):
    array_n = np.zeros((array_width, array_height), dtype=int) # re-initialize array_n as empty every time simulation is run
    for row_index, row in enumerate(array):
        for column_index, cell_0 in enumerate(row):
            cell_n = determine_new_cell_status(row_index, column_index, cell_0) # define a new cell for the array of the next generation
            array_n[row_index][column_index] = cell_n # append this new cell to its corresponding location in the new array (array_n)
    return array_n

# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

draw_grid(array_0) # draw the grid based on the size of the initial array

running = True
simulating = False

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left-click
                pos = pygame.mouse.get_pos()
                array_n = update_array_from_user_input(array_0, pos)
                array_0 = array_n
                #draw_array(array_0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                simulating = not simulating
                print("simulation", simulating)
    if simulating:
        array_n = return_new_array(array_0)
        array_0 = array_n
        #draw_array(array_0)
        sleep(0.5)
    draw_array(array_0)
 
# Quit Pygame
pygame.quit()