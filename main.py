import pygame
import numpy as np
import sys
import random
import math

import draw


class Constants():
    def __init__(self):
        self.EMPTY = 0
        # BOARD SETTINGS
        self.ROW_COUNT = 25                                             # Amount of vertical square
        self.COLUMN_COUNT = 35                                          # Amount of horizontal squares
        self.SQUARE_SIZE = 25                                           # How many pixels wide/heigh a square is
        self.SCREEN_HEIGHT = self.ROW_COUNT * self.SQUARE_SIZE          # MATH
        self.SCREEN_WIDTH = self.COLUMN_COUNT * self.SQUARE_SIZE        # MATH
        self.WINDOW_SIZE = (self.SCREEN_HEIGHT, self.SCREEN_WIDTH)      # Vector 2 for the screen size
        # COLORS
        self.COLOR_BEST_PATH = pygame.Color("#eb4034")                  # Color of the best possible path


class Variables():
    def __init__(self):
        self.screen = None                  
        self.board = None
        self.app_running = False

        self.is_first_game = True


const = Constants()
var = Variables()


# Debug tool
def print_board(board):
    print(np.flip(board, 0))


# Creats an empty board of zeros
def creat_blank_board():
    board = np.zeros(shape=(const.ROW_COUNT, const.COLUMN_COUNT), dtype=int)
    return board


if __name__ == "__main__":
    pygame.init()                                                   # Initialize Pygames
    pygame.display.set_caption('Path Finding Test')                 # Title bar message
    var.screen = pygame.display.set_mode(const.WINDOW_SIZE)         # Draw the window as var.screen

    var.app_running = True                                          # If false the program will shut down


# Starts a new serach
def new_search():
    var.board = creat_blank_board()
    # print_board(var.board)
    draw.board(var.board, const, var)

    running = True

    while running:
        # Event listeners
        for event in pygame.event.get():
            # System exiter
            if event.type == pygame.QUIT:
                sys.exit()
            # Mouse 1 click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # SELECT A POINT
                pass



# Main while loop, 
while var.app_running:
    if var.is_first_game == True:
        new_search()
    # Event listeners
    for event in pygame.event.get():
        # System exiter
        if event.type == pygame.QUIT:
            sys.exit()
        # Mouse 1 click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            new_search()