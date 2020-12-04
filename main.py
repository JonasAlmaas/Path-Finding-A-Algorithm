from numpy.lib import index_tricks
import pygame
import numpy as np
import sys
import random
import math

import draw


# MOUSE 1: Place Start and Destination location / Remove walls
# MOUSE 2: Place walls
# SPACEBAR: Run Simulation
# ESCAPE: Restart


class Constants():
    def __init__(self):
        # States
        self.STATE_1 = 1                                                                            # Pick first locarion
        self.STATE_2 = 2                                                                            # Pick second loaction
        self.STATE_3 = 3                                                                            # Ready for simulation

        self.NODE_INFO_DEPTH = 6                                                                    # Sets the depth of the node info
        # Main node info
        self.NODE_INFO_MAIN = 0                                                                     # First slot in the node array
        self.EMPTY = 0                                                                              # If there is no information on the node
        self.START_POS = 1                                                                          # Where the algorithm starts searching
        self.DESTINATION_POS = 2                                                                    # Where the algorithm wants to find the path to
        self.WALL = 3                                                                               # Index for walls
        self.HOVER = 4                                                                              # If the piece if hovered
        # Node cost
        self.NODE_INFO_G_COST = 1                                                                   # Distance from starting node
        self.NODE_INFO_H_COST = 2                                                                   # Distance from destination node
        self.NODE_INFO_F_COST = 3                                                                   # Sum of G cost and H cost
        self.NODE_INFO_PARENT = 4                                                                   # Parent node
        self.NODE_INFO_STATE = 5                                                                    # Node state
        self.NODE_STATE_OPEN = 1                                                                    # Node state open
        self.NODE_STATE_CLOSED = 2                                                                  # Node state closed

        # COLORS
        self.COLOR_TEXT = pygame.Color("#d9d9d9")                                                   # Color for text
        self.COLOR_BACKGROUND = pygame.Color("#4a4a4a")                                             # Color of the background
        self.COLOR_BLANK = pygame.Color("#2e2e2e")                                                  # Color of the enpty slots (0s in the matrix)
        self.COLOR_START_POS = pygame.Color("#2976ba")                                              # Color of the start pos
        self.COLOR_DESTINATION_POS = pygame.Color("#c97534")                                        # Color of the destination pos
        self.COLOR_WALL = pygame.Color("#1c1c1c")                                                   # Color of the walls
        self.COLOR_PATH = pygame.Color("#742880")                                                   # Color for the final path
        self.COLOR_STATE_CLOSED = pygame.Color("#bf3d3d")                                           # Color for a closed node
        self.COLOR_STATE_OPEN = pygame.Color("#5fb35f")                                             # Color for an open node

        # BOARD SETTINGS
        self.NODE_SIZE = 25                                                                         # How many pixels wide/heigh a node is
        self.MARGIN = 1                                                                             # Half the margin between node
        self.ROW_COUNT = 50                                                                         # Amount of vertical node
        self.COLUMN_COUNT = 50                                                                      # Amount of horizontal nodes
        self.SCREEN_HEIGHT = self.ROW_COUNT * (self.NODE_SIZE + self.MARGIN) + self.MARGIN          # Get the screen height from the row node size and margin
        self.SCREEN_WIDTH = self.COLUMN_COUNT * (self.NODE_SIZE + self.MARGIN) + self.MARGIN        # Get the screen width from the row node size and margin
        self.WINDOW_SIZE = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)                                  # Vector 2 for the screen size


class Variables():
    def __init__(self):
        self.screen = None                      # Screen variables
        self.board = None                       # Board variables
        self.app_running = False                # If False the program will shut down
        
        self.state = None                       # What things have been done

        self.start_node = None                  # Row and column for the start node
        self.destination_node = None             # Row and column for the destination node
        
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
    board = np.zeros(shape=(const.ROW_COUNT, const.COLUMN_COUNT, const.NODE_INFO_DEPTH), dtype=int)
    return board


def get_cost(current_node):
    row_destination_node = var.destination_node[0]
    col_destination_node = var.destination_node[1]

    row_current_node = current_node[0]
    col_current_node = current_node[1]

    # If ther is no parent, use self values for parent
    if var.board[row_current_node][col_current_node][const.NODE_INFO_PARENT] == 0:
        var.board[row_current_node][col_current_node][const.NODE_INFO_PARENT] = int(str(row_current_node) + str(col_current_node))

    parent_node = var.board[row_current_node][col_current_node][const.NODE_INFO_PARENT]
    info = [char for char in str(parent_node)]
    row_parent_node = int(info[0])
    col_parent_node = int(info[1])

    row_distance_g_cost = get_distance(row_current_node, row_parent_node)
    col_distance_g_cost = get_distance(col_current_node, col_parent_node)

    row_distance_h_cost = get_distance(row_current_node, row_destination_node)
    col_distance_h_cost = get_distance(col_current_node, col_destination_node)

    # Current node to start node
    g_cost = math.sqrt(row_distance_g_cost^2 + col_distance_g_cost^2) + var.board[row_parent_node][col_parent_node][const.NODE_INFO_G_COST]
    g_cost = math.sqrt(row_distance_g_cost^2 + col_distance_g_cost^2)
    h_cost = math.sqrt(row_distance_h_cost^2 + col_distance_h_cost^2)
    # A sum on g cost and h cost
    f_cost = g_cost + h_cost

    var.board[row_current_node][col_current_node][const.NODE_INFO_G_COST] = g_cost
    var.board[row_current_node][col_current_node][const.NODE_INFO_H_COST] = h_cost
    var.board[row_current_node][col_current_node][const.NODE_INFO_F_COST] = f_cost


def get_distance(a, b):
    big = max(a, b)
    small = min(a, b)

    distance = (big - small) * 100

    return distance


def get_lowest_f_cost(open):
    lowest_value = math.inf
    lowest_node = None
    for i in open:
        row = i[0]
        col = i[1]
        
        get_cost(i)

        if var.board[row][col][const.NODE_INFO_F_COST] < lowest_value:
            lowest_value = var.board[row][col][const.NODE_INFO_F_COST]
            lowest_node = [row, col]

    return lowest_node


def get_neighbours(current_node):
    neighbors = lambda x, y : [[x2, y2] for x2 in range(x-1, x+2) for y2 in range(y-1, y+2) if (-1 < x <= const.SCREEN_WIDTH and
    -1 < y <= const.SCREEN_HEIGHT and
    (x != x2 or y != y2) and
    (0 <= x2 <= const.SCREEN_WIDTH) and
    (0 <= y2 <= const.SCREEN_HEIGHT))]

    active_row = current_node[0]
    active_col = current_node[1]

    neighbor_list = neighbors(active_row, active_col)

    item_amount = len(neighbor_list)

    for i in range(item_amount):
        element = neighbor_list[item_amount-1-i]
        row = element[0]
        col = element[1]

        if var.board[row][col][const.NODE_INFO_MAIN] == const.WALL or var.board[row][col][const.NODE_INFO_STATE] == const.NODE_STATE_CLOSED:
            del neighbor_list[item_amount-1-i]
        else:
            var.board[row][col][const.NODE_INFO_PARENT] = int(str(active_row) + str(active_col))
    
    return neighbor_list


def a_star():
    open = []
    closed = []
    # Put the start node in the open list
    open.append(var.start_node)

    while True:
        draw.board(var.board, const, var)

        # Set current node to the node with the lowest f cost from the open list
        current_node = get_lowest_f_cost(open)

        # TODO just for debuging
        # print(current_node, var.destination_node)
        # print_board(var.board)

        # Remove current node from the open list
        index = 0
        for i in open:
            if i == current_node:
                del open[index]
            index += 1
        
        # Add current node to the closed list
        closed.append(current_node)
        var.board[current_node[0]][current_node[1]][const.NODE_INFO_STATE] = const.NODE_STATE_CLOSED

        # Check if the current node is the destination node
        if current_node == var.destination_node:
            print("Found it!")
            return
        
        # Get all valid neighbours
        neighbours = get_neighbours(current_node)
        for neighbour in neighbours:
            is_in_list = False
            for item in open:
                if item == neighbour:
                    is_in_list = True

            if is_in_list == False:
                open.append(neighbour)
                var.board[neighbour[0]][neighbour[1]][const.NODE_INFO_STATE] = const.NODE_STATE_OPEN


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
                    var.col_hover = int((event.pos[0]) / (const.NODE_SIZE + const.MARGIN))                              # Get the column the mouse is hovering
                    var.row_hover = int((event.pos[1]) / (const.NODE_SIZE + const.MARGIN))                              # Get the row the mouse is hovering
                    # Make sure the column index can't highter than the max count
                    if var.col_hover > const.COLUMN_COUNT - 1:
                        var.col_hover = const.COLUMN_COUNT - 1
                    # Make sure the row index can't highter than the max count
                    if var.row_hover > const.ROW_COUNT - 1:
                        var.row_hover = const.ROW_COUNT - 1

                    b_copy = var.board.copy()                                                                           # Make a copy of the board
                    if var.board[var.row_hover][var.col_hover][const.NODE_INFO_MAIN] == const.EMPTY:                    # Check if the hovered node is empty
                        b_copy[var.row_hover][var.col_hover][const.NODE_INFO_MAIN] = const.HOVER                        # Place the temp hovering info on the board copy

                    draw.board(b_copy, const, var)                                                                      # Redraw the board every time the mouse moves

            # Mouse 1
            if pygame.mouse.get_pressed()[0]:
                # Check that the simulation isn't running
                if not var.simulation_runngin:
                    if var.board[var.row_hover][var.col_hover][const.NODE_INFO_MAIN] == const.EMPTY:                    # Check if the selection is an empty node
                        # Place starting point
                        if var.state == const.STATE_1:                                                                  # Check if the state is the STATE_1
                            var.board[var.row_hover][var.col_hover][const.NODE_INFO_MAIN] = const.STATE_1               # Set the start pos
                            var.start_node = [var.row_hover, var.col_hover]                                             # Set the start node variable
                            var.state = const.STATE_2                                                                   # Set the state to STATE_2
                            draw.board(var.board, const, var)                                                           # Update the visible board
                        # Place destination
                        elif var.state == const.STATE_2:                                                                # Check if the state is the STATE_2
                            var.board[var.row_hover][var.col_hover][const.NODE_INFO_MAIN] = const.STATE_2               # Set the destination pos
                            var.destination_node = [var.row_hover, var.col_hover]                                       # Set the destination node variable
                            var.state = const.STATE_3                                                                   # Set the state to STATE_3
                            draw.board(var.board, const, var)                                                           # Update the visible board

                    # Remove walls
                    if var.board[var.row_hover][var.col_hover][const.NODE_INFO_MAIN] == const.WALL:                     # Check if the selected node is a wall
                        var.board[var.row_hover][var.col_hover][const.NODE_INFO_MAIN] = const.EMPTY                     # Set the destination pos
                        draw.board(var.board, const, var)                                                               # Update the visible board

            # # Mouse 2
            if pygame.mouse.get_pressed()[2]:
                # Check that the simulation isn't running
                if not var.simulation_runngin:                                                                          # Check that simulation mode is not on
                    if var.board[var.row_hover][var.col_hover][const.NODE_INFO_MAIN] == const.EMPTY:                    # Check if the selected node is EMPTY          
                        var.board[var.row_hover][var.col_hover][const.NODE_INFO_MAIN] = const.WALL                      # Set the node to a wall
                        draw.board(var.board, const, var)                                                               # Update the visible board
            
            # Check any key is pressed
            if event.type == pygame.KEYDOWN:
                # Spacebar "Start simulaton mode"
                if event.key == pygame.K_SPACE:
                    if var.state == const.STATE_3:
                        var.simulation_runngin = True
                        a_star()

                # Escape "RESET"
                if event.key == pygame.K_ESCAPE:
                    running = False


# Main while loop
while var.app_running:
    new_search()
