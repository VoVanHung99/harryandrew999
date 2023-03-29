import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 700, 500

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (52, 168, 72)
pink= (201,40,89)
yellow=(240,224,120)
orgrane=(234,120,0)
blue=(28,67,174)
bluevoilen=(142,28,212)


screen = pygame.display.set_mode(size)
mediumFont = pygame.font.SysFont('console', 28, True)
largeFont = pygame.font.SysFont('console', 40, True)
moveFont = pygame.font.SysFont('console', 60, True)
#mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
#largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
#moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(green)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, pink)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXx = (width / 8) + 10
        playXy = (height / 2)
        playXwidth = width / 4 + 15
        playXheight = 55
        playXButton = pygame.Rect(playXx, playXy , playXwidth, playXheight)
        playX = mediumFont.render("Play as X", True, orgrane)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton,0)
        for i in range(4):
          pygame.draw.rect(screen, black, (playXx-i,playXy-i,playXwidth,playXheight), 1)
        screen.blit(playX, playXRect)
        
        playYx = (width / 8) + 10
        playYy = (height / 2)
        playYwidth = width / 4 + 15
        playYheight = 55
        playOButton = pygame.Rect(4 * playYx, playYy, playYwidth, playYheight)
        playO = mediumFont.render("Play as O", True, orgrane)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton,0)
        for i in range(4):
          pygame.draw.rect(screen, black, (4*playYx-i,playYy-i,playYwidth,playYheight), 1)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    if board[i][j]== ttt.X:
                        move = moveFont.render(board[i][j], True, (253, 185, 203))
                    else:
                        move = moveFont.render(board[i][j], True, yellow)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, blue)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False 
            else:
                ai_turn = True 

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againX = width / 3
            againY =  height - 65
            againWidth = width / 3
            againHeight = 50
            againButton = pygame.Rect(againX,againY, againWidth, againHeight)
            again = mediumFont.render("Play Again", True, pink)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            for i in range(4):
              pygame.draw.rect(screen, black, (againX-i,againY-i,againWidth,againHeight), 1)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
