import pygame

import draw


class Constants():
    def __init__(self):
        self.COLUMN_AMOUNT = 35                                         # Amount of horizontal squares
        self.ROW_AMOUNT = 25                                            # Amount of vertical square
        self.SQUARE_SIZE = 25                                           # How many pixels wide/heigh a square is
        self.SCREEN_WIDTH = self.COLUMN_AMOUNT * self.SQUARE_SIZE       # MATH
        self.SCREEN_HEIGHT = self.ROW_AMOUNT * self.SQUARE_SIZE         # MATH

        self.COLOR_BEST_PATH = pygame.Color("#eb4034")                  # Color of the best possible path


class Variables():
    def __init__(self):
        self.screen = None                  
        self.board = None
        self.app_running = False

        self.is_searching = False


const = Constants()
var = Variables()


def test_print(message):
    print(message)


if __name__ == "__main__":
    test_print("Hello World")
