import pygame
import numpy as np
import sys
import random
import math

import draw


# MOUSE 1 for placeing start and end pos
# MOUSE 2 for placeing walls
# SPACEBAR to run the simulation
# ESCAPE to restart


class Constants():
    def __init__(self):
        # States
        self.STATE_1 = 1                                                                            # Pick first locarion
        self.STATE_2 = 2                                                                            # Pick second loaction
        self.STATE_3 = 3                                                                            # Ready for simulation

        self.SQUARE_INFO_DEPTH = 2                                                                  # Sets the depth of the square info
        # FIRST SLOT
        self.SQUARE_INFO_MAIN = 0                                                                   # First slot in the squares array
        self.EMPTY = 0                                                                              # If there is no information on the square
        self.START_POS = 1                                                                          # Where the algorithm starts searching
        self.DESTINATION_POS = 2                                                                    # Where the algorithm wants to find the path to
        self.WALL = 3                                                                               # Index for walls
        # SECOND SLOT
        self.SQUARE_INFO_EXTRA = 1                                                                  # Second slot in the squares array
        self.HOVER = 1                                                                              # If the piece if hovered

        # COLORS
        self.COLOR_BACKGROUND = pygame.Color("#4a4a4a")                                             # Color of the background
        self.COLOR_BLANK = pygame.Color("#2e2e2e")                                                  # Color of the enpty slots (0s in the matrix)
        self.COLOR_START_POS = pygame.Color("#2976ba")                                              # Color of the start pos
        self.COLOR_DESTINATION_POS = pygame.Color("#ba2929")                                        # Color of the destination pos
        self.COLOR_WALL = pygame.Color("#1c1c1c")                                                   # Color of the walls
        self.COLOR_PATHFINDING = pygame.Color("#00ff00")                                            # Color of the traceing

        # BOARD SETTINGS
        self.SQUARE_SIZE = 100                                                                      # How many pixels wide/heigh a square is
        self.MARGIN = 1                                                                             # Half the margin between square
        self.ROW_COUNT = 10                                                                         # Amount of vertical square
        self.COLUMN_COUNT = 15                                                                      # Amount of horizontal squares
        self.SCREEN_HEIGHT = self.ROW_COUNT * (self.SQUARE_SIZE + self.MARGIN) + self.MARGIN        # Get the screen height from the row square size and margin
        self.SCREEN_WIDTH = self.COLUMN_COUNT * (self.SQUARE_SIZE + self.MARGIN) + self.MARGIN      # Get the screen width from the row square size and margin
        self.WINDOW_SIZE = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)                                  # Vector 2 for the screen size


class Variables():
    def __init__(self):
        self.screen = None                      # Screen variables
        self.board = None                       # Board variables
        self.app_running = False                # If False the program will shut down
        
        self.state = None                       # What things have been done
        
        self.col_hover = 0                      # What column the mouse if currently hovering
        self.row_hover = 0                      # What row the mouse if currently hovering

        self.simulation_runngin = False         # Starts simulation


# Global shit
const = Constants()
var = Variables()


# Debug tool
def print_board(board):
    for r in board:
        line = ""
        for thing in r:
            info = ""
            for data in thing:
                info += str(data)
            line += str(info) + ", "
        print(line)


# Creats an empty board of zeros
def creat_blank_board():
    board = np.zeros(shape=(const.ROW_COUNT, const.COLUMN_COUNT, const.SQUARE_INFO_DEPTH), dtype=int)
    return board


if __name__ == "__main__":
    pygame.init()                                                   # Initialize Pygames
    pygame.display.set_caption('Path Finding Test')                 # Title bar message
    var.screen = pygame.display.set_mode(const.WINDOW_SIZE)         # Draw the window as var.screen
    var.screen.fill(const.COLOR_BACKGROUND)                         # Set the background color
    pygame.display.update()                                         # Refreshing the screen

    var.app_running = True                                          # If false the program will shut down


# Starts a new serach
def new_search():
    # Reset simulation mode if it is on
    if var.simulation_runngin:
        var.simulation_runngin = False

    var.board = creat_blank_board()             # Create a blank board
    draw.board(var.board, const, var)           # Display the empty board on screen
    running = True                              # Set the status to running
    var.state = const.STATE_1                   # Set the state to STATE 1

    while running:
        # Event listeners
        for event in pygame.event.get():
            # System exiter
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Mouse location
            if event.type == pygame.MOUSEMOTION:
                if not var.simulation_runngin:
                    b_copy = var.board.copy()                                                                           # Make a copy of the board
                    var.col_hover = int((event.pos[0]) / (const.SQUARE_SIZE + const.MARGIN))                            # Get the column the mouse is hovering
                    var.row_hover = int((event.pos[1]) / (const.SQUARE_SIZE + const.MARGIN))                            # Get the row the mouse is hovering
                    # Make sure the column count isn't highter than the max count
                    if var.col_hover > const.COLUMN_COUNT - 1:
                        var.col_hover = const.COLUMN_COUNT - 1
                    # Make sure the row count isn't highter than the max count
                    if var.row_hover > const.ROW_COUNT - 1:
                        var.row_hover = const.ROW_COUNT - 1

                    b_copy[var.row_hover][var.col_hover][const.SQUARE_INFO_EXTRA] = const.HOVER                         # Place the temp hovering info in the board copy
                    draw.board(b_copy, const, var)                                                                      # Draw the copied board on screen

            # Mouse 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check that the simulation isn't running
                if not var.simulation_runngin:
                    if var.board[var.row_hover][var.col_hover][const.SQUARE_INFO_MAIN] == const.EMPTY:
                        if var.state == const.STATE_1:                                                                  # Check if the state is the STATE_1
                            var.board[var.row_hover][var.col_hover][const.SQUARE_INFO_MAIN] = const.STATE_1             # Set the start pos
                            var.state = const.STATE_2                                                                   # Set the state to STATE_2
                            draw.board(var.board, const, var)                                                           # Update the visible board 
                        elif var.state == const.STATE_2:                                                                # Check if the state is the STATE_1
                            var.board[var.row_hover][var.col_hover][const.SQUARE_INFO_MAIN] = const.STATE_2             # Set the destination pos
                            var.state = const.STATE_3                                                                   # Set the state to STATE_3
                            draw.board(var.board, const, var)                                                           # Update the visible board
            
            # # Mouse 2
            if pygame.mouse.get_pressed()[2]:
                # Check that the simulation isn't running
                if not var.simulation_runngin:
                    if var.board[var.row_hover][var.col_hover][const.SQUARE_INFO_MAIN] == const.EMPTY:
                        var.board[var.row_hover][var.col_hover][const.SQUARE_INFO_MAIN] = const.WALL                    # Set the square to a wall
                        draw.board(var.board, const, var)                                                               # Update the visible board
            
            # Check if a key is pressed
            if event.type == pygame.KEYDOWN:
                # Spacebar. Start simulaton mode
                if event.key == pygame.K_SPACE:
                    if var.state == const.STATE_3:                                                                      # Check if the state is STATE_3
                        var.simulation_runngin = True

                # Backspace. Reset everything
                if event.key == pygame.K_ESCAPE:
                    running = False


# Main while loop
while var.app_running:
    new_search()
