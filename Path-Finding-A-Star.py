import pygame
import sys
import time
import math


class Constants():
    def __init__(self):
        class Node_types():
            def __init__(self):
                self.EMPTY = 0
                self.START = 1
                self.END = 2
                self.OPEN = 3
                self.CLOSED = 4
                self.PATH = 5
                self.BARRIER = 6

        class Costs():
            def __init__(self):
                self.STRAIGHT = 1
                self.DIAGONAL = 1.414213562
                # JUST FOR DEBUGGNG
                # self.STRAIGHT = 10
                # self.DIAGONAL = 14

        class Colors():
            def __init__(self):
                class Nodes():
                    def __init__(self):
                        self.EMPTY = pygame.Color("#2e2e2e")            # Grey
                        self.START = pygame.Color("#2483d6")            # Blue
                        self.END = pygame.Color("#ff9500")              # Orange
                        self.OPEN = pygame.Color("#5fb35f")             # Green
                        self.CLOSED = pygame.Color("#bf3d3d")           # Red
                        self.PATH = pygame.Color("#992bab")             # Purple
                        self.BARRIER = pygame.Color("#1c1c1c")          # Dark grey

                self.NODE = Nodes()
                self.BOARD = pygame.Color("#4a4a4a")                    # Light grey
                self.TEXT = pygame.Color("#d9d9d9")                     # White

        class Dimensions():
            def __init__(self, rows, columns):
                self.NODE_WIDTH_HEIGHT = 25
                self.NODE_MARGIN = 1
                self.WINDOW_HEIGHT = (self.NODE_WIDTH_HEIGHT + self.NODE_MARGIN) * rows
                self.WINDOW_WIDTH = (self.NODE_WIDTH_HEIGHT + self.NODE_MARGIN) * columns
                self.WINDOW_WIDTH_HEIGHT = (self.WINDOW_HEIGHT, self.WINDOW_WIDTH)

        class Keybindings():
            def __init__(self):
                # MOUSE 1 = Place/Remove start/end nodes and remove barriers
                # Mouse 2 = Place barriers
                self.SIMULATE = pygame.K_SPACE          # Run simulation
                self.RESET = pygame.K_ESCAPE            # Reset everything

        self.ROWS = 50
        self.COLUMNS = 50

        self.NODE_TYPE = Node_types()
        self.COLOR = Colors()
        self.COST = Costs()
        self.DIMENSION = Dimensions(self.ROWS, self.COLUMNS)
        self.KEYBIND = Keybindings()


class Variables():
    def __init__(self):
        class Nodes():
            def __init__(self):
                self.start = None   # Node to search from
                self.end = None      # Node you want the shortest path to

        class Simulation():
            def __init__(self):
                self.running = False
                self.done = False

        self.node = Nodes()
        self.simulation = Simulation()

        self.window = None          # The window everything is displayed in
        self.board = None           # Board matrix all that positions are stored on
        self.mouse_hover_pos = None


const = Constants()
var = Variables()


class Node():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * (const.DIMENSION.NODE_WIDTH_HEIGHT + const.DIMENSION.NODE_MARGIN)
        self.y = col * (const.DIMENSION.NODE_WIDTH_HEIGHT + const.DIMENSION.NODE_MARGIN)
        self.type = const.NODE_TYPE.EMPTY
        self.parent = None
        self.neighbors = []
        self.color = const.COLOR.NODE.EMPTY

        class Costs():
            def __init__(self):
                self.g = None           # Distance from starting node. Shortest path to parent + Parents G cost
                self.h = None           # Distance from end node
                self.f = math.inf       # Sum of G cost and H cost

        self.cost = Costs()

    def set_state(self, state: str):
        self.type = getattr(const.NODE_TYPE, state.upper())
        self.color = getattr(const.COLOR.NODE, state.upper())

    def draw(self):
        pygame.draw.rect(var.window, self.color, (self.x, self.y, const.DIMENSION.NODE_WIDTH_HEIGHT, const.DIMENSION.NODE_WIDTH_HEIGHT))

        # # JUST FOR DEBUGGNG : Drawing the costs on screen
        # # DISPLAY G COST
        # if not self.cost.g == None:
        #     font = pygame.font.SysFont(None, const.DIMENSION.NODE_WIDTH_HEIGHT // 3)
        #     txt = font.render(str(self.cost.g), True, const.COLOR.TEXT)
        #     var.window.blit(txt, (self.x, self.y))

        # # DISPLAY H COST
        # if not self.cost.h == None:
        #     font = pygame.font.SysFont(None, const.DIMENSION.NODE_WIDTH_HEIGHT // 4)
        #     txt = font.render(str(self.cost.h), True, const.COLOR.TEXT)
        #     var.window.blit(txt, (self.x + (const.DIMENSION.NODE_WIDTH_HEIGHT - const.DIMENSION.NODE_WIDTH_HEIGHT // 3), self.y))

        # # DISPLAY F COST
        # if not self.cost.f == math.inf:
        #     font = pygame.font.SysFont(None, const.DIMENSION.NODE_WIDTH_HEIGHT // 3)
        #     txt = font.render(str(self.cost.f), True, const.COLOR.TEXT)
        #     var.window.blit(txt, (self.x + const.DIMENSION.NODE_WIDTH_HEIGHT // 3, self.y + const.DIMENSION.NODE_WIDTH_HEIGHT // 2))

    def update_neighbors(self):
        self.neighbors = []
        # Set of node types to skip
        skip = {const.NODE_TYPE.START, const.NODE_TYPE.CLOSED, const.NODE_TYPE.BARRIER}

        for col in range(self.col-1, self.col+2):
            for row in range(self.row-1, self.row+2):
                # If it's the center node, aka itself
                if (self.row == row) and (self.col == col):
                    continue
                # Checks if neighbor node outside the board
                if not ((0 <= row < const.ROWS) and (0 <= col < const.COLUMNS)):
                    continue

                neighbor = var.board[row][col]
                if neighbor.type in skip:
                    continue

                parent = self.row, self.col
                g_cost, h_cost, f_cost = neighbor.get_cost(parent)

                if neighbor.cost.f > f_cost:
                    self.neighbors.append((row, col))
                    neighbor.parent = parent
                    neighbor.cost.g = g_cost
                    neighbor.cost.h = h_cost
                    neighbor.cost.f = f_cost

    def get_best_cost(self, node):
        # Nodes are expected to be a vector 2 (row, col)
        row, col = node
        # Get how many vertical and horizontal moves there are between the nodes
        vertical = abs(self.row - row)
        horizontal = abs(self.col - col)
        # Calculate how many straight and diagonal moves you need to make
        straight = abs(vertical - horizontal)
        diagonal = min(vertical, horizontal)

        # The smallest cost from one node to another
        return straight * const.COST.STRAIGHT + diagonal * const.COST.DIAGONAL

    def get_g_cost(self, parent):
        cost = self.get_best_cost(parent)

        if not parent == var.node.start:
            row, col = parent
            node = var.board[row][col]

            cost = cost + node.cost.g
        return cost

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


def draw_board():
    var.window.fill(const.COLOR.BOARD)          # Set the background color

    for row in var.board:
        for node in row:
            node.draw()

    pygame.display.update()


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
        node = var.board[row][col]
        cost = node.cost.f

        if cost < lowest_value:
            lowest_value = cost
            lowest_node = coords

    return lowest_node


def trace_path():
    row, col = var.node.end
    node = var.board[row][col]
    current_node = node.parent

    while not current_node == var.node.start:
        row, col = current_node
        node = var.board[row][col]
        node.set_state("path")
        current_node = node.parent


def a_star():
    start = time.time()
    open = []
    closed = []
    open.append(var.node.start)
    first_loop = True

    while True:
        draw_board()
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
        node = var.board[row][col]

        # Make sure to never close the start or end node
        if not current_node == var.node.start and not current_node == var.node.end:
            node.set_state("closed")

        # Check if the current node is the end node
        if current_node == var.node.end:
            end = time.time()
            trace_path()
            draw_board()
            print("Finished it in:", (end - start), "seconds")
            var.simulation.running = False
            var.simulation.done = True
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
                    node = var.board[row][col]
                    node.set_state("open")


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
                        # Reseting variables
                        var.node.start = None
                        var.node.end = None
                        var.simulation.done = False
                        # Killing the loop
                        return

                # If the simulation isn't running and it's not done
                if not var.simulation.done:
                    # Mouse position
                    if event.type == pygame.MOUSEMOTION:
                            var.mouse_hover_pos = event.pos

                    # Mouse 1
                    if pygame.mouse.get_pressed()[0]:
                        row, col = get_mouse_pos(var.mouse_hover_pos)
                        node = var.board[row][col]

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
                        # BARRIER to EMPTY
                        elif node.type == const.NODE_TYPE.BARRIER:
                            node.set_state("empty")

                        draw_board()

                    # Mouse 2
                    if pygame.mouse.get_pressed()[2]:
                        row, col = get_mouse_pos(var.mouse_hover_pos)
                        node = var.board[row][col]

                        # EMPTY to BARRIER
                        if node.type == const.NODE_TYPE.EMPTY:
                            node.set_state("barrier")

                        draw_board()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Path Finding | A-Start Algorithm')
    var.window = pygame.display.set_mode(const.DIMENSION.WINDOW_WIDTH_HEIGHT)
    pygame.display.update()

    # Main while loop
    while True:
        new_search()
