import pygame


def board(board, const, var):
    for c in range(const.COLUMN_COUNT):
        for r in range(const.ROW_COUNT):
            # Look for path
            if board[r][c][const.NODE_INFO_MAIN][0] == const.PATH:
                pygame.draw.rect(var.screen, const.COLOR_PATH, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, const.NODE_SIZE, const.NODE_SIZE))

            # Mark closed nodes
            elif board[r][c][const.NODE_INFO_STATE][0] == const.NODE_STATE_CLOSED:
                pygame.draw.rect(var.screen, const.COLOR_STATE_CLOSED, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, const.NODE_SIZE, const.NODE_SIZE))

            # Mark open nodes
            elif board[r][c][const.NODE_INFO_STATE][0] == const.NODE_STATE_OPEN:
                pygame.draw.rect(var.screen, const.COLOR_STATE_OPEN, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, const.NODE_SIZE, const.NODE_SIZE))

            # Make a background
            elif board[r][c][const.NODE_INFO_MAIN][0] == const.EMPTY:
                pygame.draw.rect(var.screen, const.COLOR_BLANK, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, const.NODE_SIZE, const.NODE_SIZE))
            
            # Hovering over node
            elif board[r][c][const.NODE_INFO_MAIN][0] == const.HOVER:
                    pygame.draw.rect(var.screen, const.COLOR_BACKGROUND, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, const.NODE_SIZE, const.NODE_SIZE))
            
            # Look for a wall
            elif board[r][c][const.NODE_INFO_MAIN][0] == const.WALL:
                pygame.draw.rect(var.screen, const.COLOR_WALL, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, const.NODE_SIZE, const.NODE_SIZE))


            # Look for start pos
            if board[r][c][const.NODE_INFO_MAIN][0] == const.START_POS:
                pygame.draw.rect(var.screen, const.COLOR_START_POS, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, const.NODE_SIZE, const.NODE_SIZE))
            
            # Look for destingation pos
            elif board[r][c][const.NODE_INFO_MAIN][0] == const.DESTINATION_POS:
                pygame.draw.rect(var.screen, const.COLOR_DESTINATION_POS, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, const.NODE_SIZE, const.NODE_SIZE))
            

            # # Display F cost
            # if board[r][c][const.NODE_INFO_F_COST][0]:
            #     font = pygame.font.SysFont(None, 35)
            #     txt = font.render(str(board[r][c][const.NODE_INFO_F_COST][0]), True, const.COLOR_TEXT)
            #     var.screen.blit(txt, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN + const.NODE_SIZE / 3, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN + (const.NODE_SIZE - 35)))

            # # Display G cost
            # if board[r][c][const.NODE_INFO_G_COST][0]:
            #     font = pygame.font.SysFont(None, 20)
            #     txt = font.render(str(board[r][c][const.NODE_INFO_G_COST][0]), True, const.COLOR_TEXT)
            #     var.screen.blit(txt, (c * (const.NODE_SIZE + const.MARGIN) + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN))

            # # Display H cost
            # if board[r][c][const.NODE_INFO_H_COST][0]:
            #     font = pygame.font.SysFont(None, 20)
            #     txt = font.render(str(board[r][c][const.NODE_INFO_H_COST][0]), True, const.COLOR_TEXT)
            #     var.screen.blit(txt, (c * (const.NODE_SIZE + const.MARGIN) + (const.NODE_SIZE / 3) * 2 + const.MARGIN, r * (const.NODE_SIZE + const.MARGIN) + const.MARGIN))


    pygame.display.update()