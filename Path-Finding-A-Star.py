import pygame
import sys
import time
import math
import random
import ctypes

user32 = ctypes.windll.user32


# Indexes for all the different nodes
class Node_types():
    def __init__(self):
        self.EMPTY = 0
        self.START = 1
        self.END = 2
        self.OPEN = 3
        self.CLOSED = 4
        self.PATH = 5
        self.BARRIER = 6


# Cost for different moves
class Move_cost():
    def __init__(self):
        self.STRAIGHT = 1
        self.DIAGONAL = 1.414213562


# Dimentions for things to be drawn
class Dimensions():
    def __init__(self, rows, columns):
        self.SCREEN_WIDTH = user32.GetSystemMetrics(1)- 150
        # self.NODE_WIDTH_HEIGHT = 25
        self.NODE_WIDTH_HEIGHT = self.SCREEN_WIDTH // rows
        self.NODE_MARGIN = 0
        self.WINDOW_HEIGHT = (self.NODE_WIDTH_HEIGHT + self.NODE_MARGIN) * rows
        self.WINDOW_WIDTH = (self.NODE_WIDTH_HEIGHT + self.NODE_MARGIN) * columns
        self.WINDOW_WIDTH_HEIGHT = (self.WINDOW_HEIGHT, self.WINDOW_WIDTH)


# Colors for the different nodes
class Node_colors():
    def __init__(self):
        self.EMPTY = pygame.Color("#393939")        # Grey
        self.START = pygame.Color("#4294db")        # Blue
        self.END = pygame.Color("#ffab36")          # Orange
        self.OPEN = pygame.Color("#6cb86c")         # Green
        self.CLOSED = pygame.Color("#c95353")       # Red
        self.PATH = pygame.Color("#bb00ff")         # Purple
        self.BARRIER = pygame.Color("#242424")      # Dark grey


# Main color class
class Colors():
    def __init__(self):
        self.NODE = Node_colors()
        self.BOARD = pygame.Color("#4d4d4d")        # Light grey
        self.TEXT = pygame.Color("#d9d9d9")         # White


class Keybindings():
    def __init__(self):
        # MOUSE 1 = Place/Remove start/end nodes and remove barriers
        # Mouse 2 = Place barriers
        self.SIMULATE = pygame.K_SPACE          # Run simulation
        self.GENERATE_MAZE = pygame.K_g         # Generate maze
        self.RESET = pygame.K_ESCAPE            # Reset everything


# Main constants class 
class Constants():
    def __init__(self):
        self.REALTIME_DRAW = True
        self.ROWS = 50
        self.COLUMNS = 50

        self.NODE_TYPE = Node_types()
        self.COLOR = Colors()
        self.COST = Move_cost()
        self.DIMENSION = Dimensions(self.ROWS, self.COLUMNS)
        self.KEYBIND = Keybindings()


class Node_variables():
    def __init__(self):
        self.start = None       # Node to search from
        self.end = None         # Node you want the shortest path to


class Simulation_variables():
    def __init__(self):
        self.running = False
        self.done = False


# Main variables class 
class Variables():
    def __init__(self):
        self.window = None          # The window everything is displayed in
        self.board = None           # Board matrix all that positions are stored on
        self.mouse_hover_pos = None

        self.node = Node_variables()
        self.simulation = Simulation_variables()


# Global objects
const = Constants()
var = Variables()


# The different cost values for each node
class Node_cost():
    def __init__(self):
        self.g = None           # Distance from starting node. Shortest path to parent + Parents G cost
        self.h = None           # Distance from end node
        self.f = math.inf       # Sum of G cost and H cost


# Information about the location of the node
class Node_pos():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * (const.DIMENSION.NODE_WIDTH_HEIGHT + const.DIMENSION.NODE_MARGIN)
        self.y = col * (const.DIMENSION.NODE_WIDTH_HEIGHT + const.DIMENSION.NODE_MARGIN)


# The main node class
class Node():
    def __init__(self, row, col):
        self.type = const.NODE_TYPE.EMPTY       # Setting the node to an empty node type
        self.color = const.COLOR.NODE.EMPTY     # Setting node color to the color of an empty node
        self.parent = None                      # A tuple containing the row and col for the parent node
        self.neighbors = []                     # A list of all the nodes neighbors
        self.pos = Node_pos(row, col)           # Information about the position of the node (row, col, x, y)
        self.cost = Node_cost()                 # Information about the cost values for the node (g, h, f)

    # Input the type of a node you wanna make it. example: node.set_state("open")
    def set_state(self, state: str):
        self.type = getattr(const.NODE_TYPE, state.upper())
        self.color = getattr(const.COLOR.NODE, state.upper())

    # Make the node ready to be drawn on the next update
    def draw(self):
        pygame.draw.rect(var.window, self.color, (self.pos.x, self.pos.y, const.DIMENSION.NODE_WIDTH_HEIGHT, const.DIMENSION.NODE_WIDTH_HEIGHT))

    # Update the list of valid neighbors
    def update_neighbors(self):
        self.neighbors = []
        # Set of node types to skip
        skip = {const.NODE_TYPE.START, const.NODE_TYPE.CLOSED, const.NODE_TYPE.BARRIER}

        # Check a 3x3 grid around itself
        for col in range(self.pos.col - 1, self.pos.col + 2):
            for row in range(self.pos.row - 1, self.pos.row + 2):
                # If it's itself
                if (self.pos.row == row) and (self.pos.col == col):
                    continue
                # If the neighbor is not on the board
                if not ((0 <= row < const.ROWS) and (0 <= col < const.COLUMNS)):
                    continue

                # Get the node object for the neighbor
                neighbor = get_node_object(row, col)
                # Check if the node is one of the nodes to be skiped
                if neighbor.type in skip:
                    continue
                
                # Get the cost from the neighbor to self
                g_cost, h_cost, f_cost = neighbor.get_cost((self.pos.row, self.pos.col))

                # Check if the new cost is lower than the old one
                if neighbor.cost.f > f_cost:
                    self.neighbors.append((row, col))               # Add the tuple of coords to the neighbors list
                    neighbor.parent = self.pos.row, self.pos.col    # Set the parent tuple the the self position
                    # Set all the new cost values
                    neighbor.cost.g = g_cost
                    neighbor.cost.h = h_cost
                    neighbor.cost.f = f_cost

    def get_best_cost(self, node):
        # Nodes are expected to be a vector 2 (row, col)
        row, col = node
        # Get how many vertical and horizontal moves there are between the nodes
        vertical = abs(self.pos.row - row)
        horizontal = abs(self.pos.col - col)
        # Calculate how many straight and diagonal moves you need to make (For the optimal path)
        straight = abs(vertical - horizontal)
        diagonal = min(vertical, horizontal)

        # The smallest cost from one self to another node
        return straight * const.COST.STRAIGHT + diagonal * const.COST.DIAGONAL

    # Distance from starting node
    def get_g_cost(self, parent):
        cost = self.get_best_cost(parent)

        if not parent == var.node.start:
            row, col = parent
            node = get_node_object(row, col)
            node = get_node_object(row, col)

            cost = cost + node.cost.g
        return cost

    # Get the newes costs and return all of them as a vector3. This function does not update the cost variables for the node
    def get_cost(self, parent):
        g_cost = self.get_g_cost(parent)
        h_cost = self.get_best_cost(var.node.end)
        return g_cost, h_cost, g_cost + h_cost


def create_board():
    board = []
    for row in range(const.ROWS):
        board.append([])
        for col in range(const.COLUMNS):
            node = Node(row, col)
            board[row].append(node)
    return board


# Resets all variables
def reset():
    # Reseting variables
    var.node.start = None
    var.node.end = None
    var.simulation.done = False
    var.simulation.running = False


# Display the currect board matrix on the screen
def draw_board():
    var.window.fill(const.COLOR.BOARD)

    for row in var.board:
        for node in row:
            node.draw()

    pygame.display.update()


def get_node_object(row, col):
    return var.board[row][col]


def get_mouse_pos(pos):
    x, y = pos
    row = x // (const.DIMENSION.NODE_WIDTH_HEIGHT + const.DIMENSION.NODE_MARGIN)
    col = y // (const.DIMENSION.NODE_WIDTH_HEIGHT + const.DIMENSION.NODE_MARGIN)
    return row, col


def get_lowest_f_cost(list_open):
    lowest_value = math.inf
    lowest_node = None

    for coords in list_open:
        if coords == var.node.end:
            return coords

        row, col = coords
        node = get_node_object(row, col)
        cost = node.cost.f

        if cost < lowest_value:
            lowest_value = cost
            lowest_node = coords

    return lowest_node


# Trace back the path starting from the end node. Call this ones the fastest path has been found.
def trace_path():
    row, col = var.node.end
    end_node = get_node_object(row, col)
    current_node = end_node.parent

    while not current_node == var.node.start:
        row, col = current_node
        node = get_node_object(row, col)
        node.set_state("path")
        current_node = node.parent


# Set the correct variables values ones the simulation is no longer running
def simulation_end(timer_start):
    timer_end = time.time()
    print("Finished in", round((timer_end - timer_start), 3), "seconds")
    var.simulation.running = False
    var.simulation.done = True


def a_star():
    # Start a timer to see how long it takes to find the fastest path
    timer_start = time.time()
    # Make some empty lists
    open = []
    closed = []
    # Add the starting node to the open list
    open.append(var.node.start)
    first_loop = True

    while True:
        # Check if the open list is empty
        if open == []:
            print("No valid paths")
            simulation_end(timer_start)
            draw_board()
            return

        if not first_loop:
            # Set the current node to the node in the open list with the lowest F cost
            current_node = get_lowest_f_cost(open)
        else:
            first_loop = False
            current_node = var.node.start

        # Remove current node from the open list
        open.remove(current_node)
        # Add current node to the closed list
        closed.append(current_node)

        # Get the node object
        row, col = current_node
        node = get_node_object(row, col)

        # Make sure to never close the start or end node
        if not current_node == var.node.start and not current_node == var.node.end:
            node.set_state("closed")

        # Check if the current node is the end node
        if current_node == var.node.end:
            simulation_end(timer_start)
            trace_path()
            draw_board()
            return

        # Get all valid neighbors
        node.update_neighbors()
        neighbors = node.neighbors
        for neighbor in neighbors:
            is_in_list = False
            for item in open:
                if item == neighbor:
                    is_in_list = True

            if not is_in_list:
                open.append(neighbor)
                if not neighbor == var.node.end:
                    # Get the node object for the neighbor
                    row, col = neighbor
                    node = get_node_object(row, col)
                    node.set_state("open")
        
        if const.REALTIME_DRAW:
            draw_board()


def get_maze_neighbors_4(row, col):
    neighbors = []

    for neighbor in [(row + 1, col), (row, col + 1), (row -1, col), (row, col - 1)]:
        row2, col2 = neighbor
        # If the neighbor is not on the board
        if not ((0 <= row2 < const.ROWS) and (0 <= col2 < const.COLUMNS)):
            continue
        
        neighbors.append(neighbor)

    return neighbors


def get_maze_neighbors_8(row1, col1):
    neighbors = []

    for col in range(col1 - 1, col1 + 2):
        for row in range(row1 - 1, row1 + 2):
            # If it's itself
            if (row1 == row) and (col1 == col):
                continue
            # If the neighbor is not on the board
            if not ((0 <= row < const.ROWS) and (0 <= col < const.COLUMNS)):
                continue

            neighbors.append((row, col))

    return neighbors


def generare_maze():
    reset()
    var.board = create_board()

    valid_neighbors = []

    # Make everything barriers
    for row in range(const.ROWS):
        for col in range(const.COLUMNS):
            node = var.board[row][col]
            node.set_state("barrier")

    # Get a random start pos
    row = random.randint(0, const.ROWS - 1)
    col = random.randint(0, const.COLUMNS - 1)

    # Starting point
    # row = 0
    # col = 0

    valid_neighbors.append((row, col))

    node = get_node_object(row, col)
    node.set_state("empty")

    while not valid_neighbors == []:
        # Get a random neighbor
        main_neighbor = random.choice(valid_neighbors)
        valid_neighbors.remove(main_neighbor)

        row2, col2 = main_neighbor

        # Get it's neighbors
        new_neighbors = get_maze_neighbors_4(row2, col2)

        for new_neighbor in new_neighbors:
            row3, col3 = new_neighbor
            neighbors = get_maze_neighbors_8(row3, col3)

            assume_all_barriers = True
            for neighbor in neighbors:
                row4, col4 = neighbor

                node = get_node_object(row4, col4)
                
                # If the node is not the active node
                if not (row4, col4) == (row, col):
                    # If the neighbor is a not barrier
                    if not node.type == const.NODE_TYPE.BARRIER:
                        assume_all_barriers = False

            if assume_all_barriers == True:
                node = get_node_object(row2, col2)
                node.set_state("empty")

                for neighbor in new_neighbors:
                    valid_neighbors.append(neighbor)


def new_search():
    var.board = create_board()
    draw_board()

    while True:
        # Event listeners
        for event in pygame.event.get():
            # System exiter
            if event.type == pygame.QUIT:
                sys.exit()

            if not var.simulation.running:
                # Check for any key presses
                if event.type == pygame.KEYDOWN:
                    if event.key == const.KEYBIND.SIMULATE:
                        if not var.node.start == None and not var.node.end == None and not var.simulation.done:
                            var.simulation.running = True
                            a_star()

                    # Reset everything
                    if event.key == const.KEYBIND.RESET:
                        reset()
                        # Killing the loop
                        return
                    
                    if event.key == const.KEYBIND.GENERATE_MAZE:
                        generare_maze()
                        draw_board()

                # If the simulation isn't running and it's not done
                if not var.simulation.done:
                    # Mouse position
                    if event.type == pygame.MOUSEMOTION:
                            var.mouse_hover_pos = event.pos

                    # Mouse button 1 (Fire ones when presses)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        row, col = get_mouse_pos(var.mouse_hover_pos)
                        node = get_node_object(row, col)

                        # EMPTY to START when there is no other START
                        if node.type == const.NODE_TYPE.EMPTY and var.node.start == None:
                            var.node.start = row, col
                            node.set_state("start")
                        # START TO EMPTY
                        elif node.type == const.NODE_TYPE.START:
                            var.node.start = None
                            node.set_state("empty")
                        # EMPTY to END when there is no other END
                        elif node.type == const.NODE_TYPE.EMPTY and var.node.end == None:
                            var.node.end = row, col
                            node.set_state("end")
                        # END TO EMPTY
                        elif node.type == const.NODE_TYPE.END:
                            var.node.end = None
                            node.set_state("empty")

                        draw_board()

                    # Mouse 1 (Fiers as long as the button is held down)
                    if pygame.mouse.get_pressed()[0]:
                        row, col = get_mouse_pos(var.mouse_hover_pos)
                        node = get_node_object(row, col)

                        # BARRIER to EMPTY
                        if node.type == const.NODE_TYPE.BARRIER:
                            node.set_state("empty")

                        draw_board()

                    # Mouse 2
                    if pygame.mouse.get_pressed()[2]:
                        row, col = get_mouse_pos(var.mouse_hover_pos)
                        node = get_node_object(row, col)

                        # EMPTY to BARRIER
                        if node.type == const.NODE_TYPE.EMPTY:
                            node.set_state("barrier")

                        draw_board()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Path Finding | A-Start Algorithm')
    var.window = pygame.display.set_mode(const.DIMENSION.WINDOW_WIDTH_HEIGHT)

    # Main while loop
    while True:
        new_search()
