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
                # JUST FOR DEBUGING
                # self.STRAIGHT = 10
                # self.DIAGONAL = 14

        class Colors():
            def __init__(self):
                class Nodes():
                    def __init__(self):
                        self.EMPTY = pygame.Color("#2e2e2e")            # Grey
                        self.START = pygame.Color("#2976ba")            # Blue
                        self.END = pygame.Color("#c97534")              # Orange
                        self.OPEN = pygame.Color("#5fb35f")             # Green
                        self.CLOSED = pygame.Color("#bf3d3d")           # Red
                        self.PATH = pygame.Color("#742880")             # Purple
                        self.BARRIER = pygame.Color("#1c1c1c")          # Dark grey
                
                self.NODE = Nodes()
                self.BOARD = pygame.Color("#4a4a4a")                    # Light grey
                self.TEXT = pygame.Color("#d9d9d9")                     # White

        class Dimentions():
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
        self.DIMENTIONS = Dimentions(self.ROWS, self.COLUMNS)
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
        self.x = row * (const.DIMENTIONS.NODE_WIDTH_HEIGHT + const.DIMENTIONS.NODE_MARGIN)
        self.y = col * (const.DIMENTIONS.NODE_WIDTH_HEIGHT + const.DIMENTIONS.NODE_MARGIN)
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

    def make_open(self):
        self.type = const.NODE_TYPE.OPEN
        self.color = const.COLOR.NODE.OPEN

    def make_closed(self):
        self.type = const.NODE_TYPE.CLOSED
        self.color = const.COLOR.NODE.CLOSED

    def make_barrier(self):
        self.type = const.NODE_TYPE.BARRIER
        self.color = const.COLOR.NODE.BARRIER

    def make_start(self):
        self.type = const.NODE_TYPE.START
        self.color = const.COLOR.NODE.START

    def make_end(self):
        self.type = const.NODE_TYPE.END
        self.color = const.COLOR.NODE.END
    
    def make_path(self):
        self.type = const.NODE_TYPE.PATH
        self.color = const.COLOR.NODE.PATH

    def make_empty(self):
        self.type = const.NODE_TYPE.EMPTY
        self.color = const.COLOR.NODE.EMPTY

    def draw(self):
        pygame.draw.rect(var.window, self.color, (self.x, self.y, const.DIMENTIONS.NODE_WIDTH_HEIGHT, const.DIMENTIONS.NODE_WIDTH_HEIGHT))

        # JUST FOR DEBUGING
        # # DISPLAY G COST
        # if not self.cost.g == None:
        #     font = pygame.font.SysFont(None, const.DIMENTIONS.NODE_WIDTH_HEIGHT // 3)
        #     txt = font.render(str(self.cost.g), True, const.COLOR.TEXT)
        #     var.window.blit(txt, (self.x, self.y))

        # # DISPLAY H COST
        # if not self.cost.h == None:
        #     font = pygame.font.SysFont(None, const.DIMENTIONS.NODE_WIDTH_HEIGHT // 4)
        #     txt = font.render(str(self.cost.h), True, const.COLOR.TEXT)
        #     var.window.blit(txt, (self.x + (const.DIMENTIONS.NODE_WIDTH_HEIGHT - const.DIMENTIONS.NODE_WIDTH_HEIGHT // 3), self.y))

        # # DISPLAY F COST
        # if not self.cost.f == math.inf:
        #     font = pygame.font.SysFont(None, const.DIMENTIONS.NODE_WIDTH_HEIGHT // 3)
        #     txt = font.render(str(self.cost.f), True, const.COLOR.TEXT)
        #     var.window.blit(txt, (self.x + const.DIMENTIONS.NODE_WIDTH_HEIGHT // 3, self.y + const.DIMENTIONS.NODE_WIDTH_HEIGHT // 2))

    def update_neighbors(self):
        self.neighbors = []
        for col2 in range(self.col-1, self.col+2):
            for row2 in range(self.row-1, self.row+2):
                if (self.row == row2) and (self.col == col2):                               # If it's the center node, aka it self 
                    continue
                if not ((0 <= row2 < const.ROWS) and (0 <= col2 < const.COLUMNS)):          # Checks if neighbor node outside the board
                    continue
                if (row2, col2) == var.node.start:
                    continue

                neighbor = var.board[row2][col2]
                if neighbor.type == const.NODE_TYPE.CLOSED:
                    continue
                if neighbor.type == const.NODE_TYPE.BARRIER:
                    continue
                
                parent = self.row, self.col
                g_cost, h_cost, f_cost = neighbor.get_cost(parent)

                if neighbor.cost.f > f_cost:
                    self.neighbors.append((row2, col2))
                    neighbor.parent = parent
                    neighbor.cost.g = g_cost
                    neighbor.cost.h = h_cost
                    neighbor.cost.f = f_cost

    def get_best_cost(self, node2):
        # Nodes are expected to be a vector 2 (row, col)
        row2, col2 = node2
        # Get how many vertical and horizontal moves there are between the nodes
        vertical = max(self.row, row2) - min(self.row, row2)
        horizontal = max(self.col, col2) - min(self.col, col2)
        # Calculate how many straight and diagonal moves you need to make
        straight = max(vertical, horizontal) - min(vertical, horizontal)
        diagonal = max(vertical, horizontal) - straight

        # JUST FOR DEBUGING
        # print("Node 1 pos:", row1, col1)
        # print("Node 2 pos:", row2, col2)
        # print("Vertical move(s):", vertical)
        # print("Horizontal move(s):", horizontal)
        # print("Straight mode(s):", straight)
        # print("Diagonal move(s):", diagonal)

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
    for row in range(0, const.ROWS):
        board.append([])
        for col in range(0, const.COLUMNS):
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
    row = x // (const.DIMENTIONS.NODE_WIDTH_HEIGHT + const.DIMENTIONS.NODE_MARGIN)
    col = y // (const.DIMENTIONS.NODE_WIDTH_HEIGHT + const.DIMENTIONS.NODE_MARGIN)
    return row, col


def get_lowest_f_cost(list):
    lowest_value = math.inf
    lowest_node = None
    for i in list:
        if i == var.node.end:
            return i
        row, col = i
        node = var.board[row][col]
        cost = node.cost.f
        if cost < lowest_value:
            lowest_value = cost
            lowest_node = i
    return lowest_node


def trance_path():
    row, col = var.node.end
    node = var.board[row][col]
    current_node = node.parent

    while not current_node == var.node.start:
        row, col = current_node
        node = var.board[row][col]
        node.make_path()
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
            node.make_closed()

        # Check if the current node is the end node
        if current_node == var.node.end:
            end = time.time()
            trance_path()
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
                    node.make_open()


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
                            node.make_start()
                        # START TO EMPTY
                        elif node.type == const.NODE_TYPE.START:
                            var.node.start = None
                            node.make_empty()
                        # EMPTY to END when there is no other END
                        elif node.type == const.NODE_TYPE.EMPTY and var.node.end == None:
                            var.node.end = row, col
                            node.make_end()
                        # END TO EMPTY
                        elif node.type == const.NODE_TYPE.END:
                            var.node.end = None
                            node.make_empty()
                        # BARRIER to EMPTY
                        elif node.type == const.NODE_TYPE.BARRIER:
                            node.make_empty()
                        
                        draw_board()

                    # Mouse 2
                    if pygame.mouse.get_pressed()[2]:
                        row, col = get_mouse_pos(var.mouse_hover_pos)
                        node = var.board[row][col]

                        # EMPTY to BARRIER
                        if node.type == const.NODE_TYPE.EMPTY:
                            node.make_barrier()

                        draw_board()
                        

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Path Finding | A-Start Algorithm')
    var.window = pygame.display.set_mode(const.DIMENTIONS.WINDOW_WIDTH_HEIGHT)
    pygame.display.update()


# Main while loop
while True:
    new_search()
