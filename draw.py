import pygame

def board(board, const, var):
    for c in range(const.COLUMN_COUNT):
        for r in range(const.ROW_COUNT):
            # Make a background
            if board[r][c][const.SQUARE_INFO_MAIN] == const.EMPTY:
                pygame.draw.rect(var.screen, const.COLOR_BLANK, (c * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, r * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, const.SQUARE_SIZE, const.SQUARE_SIZE))
                # If the board square is empty and the mouse if hovering
                if board[r][c][const.SQUARE_INFO_EXTRA] == const.HOVER:
                    pygame.draw.rect(var.screen, const.COLOR_BACKGROUND, (c * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, r * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, const.SQUARE_SIZE, const.SQUARE_SIZE))
            # Look for start pos
            elif board[r][c][const.SQUARE_INFO_MAIN] == const.START_POS:
                pygame.draw.rect(var.screen, const.COLOR_START_POS, (c * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, r * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, const.SQUARE_SIZE, const.SQUARE_SIZE))
            # Look for destingation pos
            elif board[r][c][const.SQUARE_INFO_MAIN] == const.DESTINATION_POS:
                pygame.draw.rect(var.screen, const.COLOR_DESTINATION_POS, (c * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, r * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, const.SQUARE_SIZE, const.SQUARE_SIZE))
            # Look for a wall
            elif board[r][c][const.SQUARE_INFO_MAIN] == const.WALL:
                pygame.draw.rect(var.screen, const.COLOR_WALL, (c * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, r * (const.SQUARE_SIZE + const.MARGIN) + const.MARGIN, const.SQUARE_SIZE, const.SQUARE_SIZE))


    pygame.display.update()