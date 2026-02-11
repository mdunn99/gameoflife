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

array_width, array_height = 16, 16 # configure the size of an array
screen_width, screen_height = 720, 720 # configure the size of the screen
ratio_of_screen_to_area = 2 # how much smaller should the area of the array be in relation to the screen?
area_width, area_height = screen_width/ratio_of_screen_to_area, screen_height/ratio_of_screen_to_area # define an area where the array will be imposed
array_0 = np.zeros((array_width, array_height), dtype=int) # initialize initial array as empty

# superimposing the array onto the area
cell_width, cell_height = area_width/array_width, area_height/array_height

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
def get_array_indices():
    screen_position_y, screen_position_x = pygame.mouse.get_pos() # returns as height, width
    pos_on_grid = screen_position_y-area_height/ratio_of_screen_to_area, screen_position_x-area_width/ratio_of_screen_to_area
    row = int(pos_on_grid[1] // cell_height)
    cell = int(pos_on_grid[0] // cell_width)
    array_index = (row, cell)
    return array_index, pos_on_grid

# update array value associated with position clicked
def update_array_from_user_input(array_to_update):
    array = np.copy(array_to_update)
    array_index, pos = get_array_indices()
    print(f"\nmouse clicked at position: {pos}")

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
        for cell_i, _ in enumerate(row):

            pos_x = cell_i*cell_width # the nth cell in the array times the width (in pixels) is the horizontal position of the grid line
            pos_x = pos_x+area_width/ratio_of_screen_to_area # center the drawn array (idk how this works)

            pos_y = row_i*cell_height # the nth cell in the array times the height (in pixels) is the vertical position of the grid line
            pos_y = pos_y+area_height/ratio_of_screen_to_area

            # draw the upper vertical grid
            pygame.draw.rect(screen, (255,255,255),
                            pygame.Rect(pos_x,pos_y,1,cell_height)) # horiz. pos. in pixels,vert. pos. in pixels,thin width,height (vertical line)
            # draw the horizontal grid
            pygame.draw.rect(screen, (255,255,255),
                            pygame.Rect(pos_x,pos_y,cell_width,1)) # horiz. pos. in pixels,vert. pos. in pixels,width,thin height (horizontal line)
    return #pygame.display.flip()

def draw_array(array):
    for row_i, row in enumerate(array):
        for cell_i, cell in enumerate(row):
            
            pos_x = cell_i*cell_width
            #pos_x = pos_x+area_width/ratio_of_screen_to_area

            pos_y = row_i*cell_height
            #pos_y = pos_y+area_height/ratio_of_screen_to_area

            # if the cell is active, draw it as such!
            if cell == 1:
                # making the size of the cells "*0.90" makes the cells slightly smaller than the
                # size of the whole cell, allowing the grid lines to be visible.
                # we have to adjust the position accordingly, so we add a buffer buffer_px to each coordinate for the cells

                pygame.draw.rect(screen, white,
                                pygame.Rect(pos_x+buffer_px,pos_y+buffer_px,cell_width*0.90,cell_height*0.90))

            else:
                pygame.draw.rect(screen, black,
                                pygame.Rect(pos_x+buffer_px,pos_y+buffer_px,cell_width*0.90,cell_height*0.90))

    return #pygame.display.flip()

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
generations = 0

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left-click
                array_n = update_array_from_user_input(array_0)
                array_0 = array_n
                #draw_array(array_0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                simulating = not simulating
                print("simulation", simulating)
    if simulating:
        print("generation:", generations)
        array_n = return_new_array(array_0)
        array_0 = array_n
        #draw_array(array_0)
        sleep(0.1)
        generations += 1
    if not simulating:
        generations = 0
    draw_array(array_0)
    pygame.display.flip()
    clock.tick(60)
 
# Quit Pygame
pygame.quit()