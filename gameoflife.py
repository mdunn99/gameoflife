from time import sleep
from termcolor import colored
import numpy as np
import pylab as plt
import logging

'''
logger = logging.getLogger(__name__)

logging.basicConfig(
    filename='conway.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)
logger.info('Started')
'''

im = None
plt.grid()

# t_initial (ABITRARY)
t_0 = np.array([[0,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0],
                    [1,1,1,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]])

# logger.info(f'Initialize t_0 with length of {len(t_0)}: {t_0[0:1]}...')

def count_live_cells(row, column):
    # get around python negative indices
    # if the row value is the minimum or maximum, 
    # assume that the outer cells are dead
    live_cells = 0
    try:
        live_cells += t_0[row-1][column] if row != 0 else 0             # up
        live_cells += t_0[row-1][column+1] if row != 0 else 0           # up right
        live_cells += t_0[row][column+1] # will get caught by error     # right
        live_cells += t_0[row+1][column+1] if row != len(t_0)-1 else 0  # down right
        live_cells += t_0[row+1][column] if row != len(t_0)-1 else 0    # down
        live_cells += t_0[row+1][column-1] if row != len(t_0)-1 else 0  # down left
        live_cells += t_0[row][column-1] # will get caught by error     # left
        live_cells += t_0[row-1][column-1]                              # up left
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

def get_data():
    for row_index, row in enumerate(t_0):
        for column_index, cell_0 in enumerate(row):
            cell_n = determine_new_cell_status(row_index, column_index, cell_0) # define a new cell for the matrix of the next generation
            t_n[row_index][column_index] = cell_n # append this new cell to its corresponding location in the new matrix
    return t_n

while True:
    generation = 0
    for _ in range(len(t_0)): # iterate this loop for the length of initial matrix (rows)
        generation += 1
        print(f'Generation(s): {generation}')
        # logger.info(f'Generation: {generation}')

        # initialize "t new" as a matrix of 0s
        t_n = np.array([[0 for i in range(len(t_0))] for i in range(len(t_0))])
        # logger.info(f"Initialize t_n with length of {len(t_n)}: {t_n[0:1]}")

        if not im:
            # generate plot first time
            im = plt.imshow(get_data(), cmap = 'grey', interpolation='none')
            # plt.figtext(0.2, 0.01, f'Generation(s): {generation}', wrap=True, horizontalalignment='center')
        else:
            im.set_data(get_data())
        plt.draw()
        plt.pause(0.1)
        print(*t_n,sep='\n')
        # logger.debug(f"t_0: {t_0}")
        t_0 = t_n
        # logger.info(f"t_0: {t_0}")
        print('\n')