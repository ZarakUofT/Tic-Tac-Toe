import pygame
import os
import time
import random
import ctypes
pygame.font.init()
pygame.init()

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
WRONG_CLICK = False

LINE_AD_X = 0.4
LINE_AD_Y = 0.2

HUMAN = 'O'
AI = 'X'

CURRENT_PLAYER = HUMAN
AI_FIRST = False

SCORE = {'O': -1,
         'X': 1,
         'tie': 0
        }

def mark_placement_pos_find(left, right, top, bottom):
    x = (right - left)/2
    y = (bottom - top)/2
    return (left + x, top + y)

ENTRY_POS = {1: mark_placement_pos_find(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
             2: mark_placement_pos_find(WIDTH * LINE_AD_X, WIDTH * (1 - LINE_AD_X), HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
             3: mark_placement_pos_find(WIDTH * (1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), HEIGHT*LINE_AD_Y, HEIGHT*LINE_AD_X),
             4: mark_placement_pos_find(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, HEIGHT*LINE_AD_X, HEIGHT*(1 - LINE_AD_X)),
             5: mark_placement_pos_find(WIDTH * LINE_AD_X, WIDTH * (1 - LINE_AD_X), HEIGHT*LINE_AD_X, HEIGHT*(1 - LINE_AD_X)),
             6: mark_placement_pos_find(WIDTH * (1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), HEIGHT*LINE_AD_X, HEIGHT*(1 - LINE_AD_X)),
             7: mark_placement_pos_find(WIDTH*LINE_AD_Y, WIDTH * LINE_AD_X, HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y)),
             8: mark_placement_pos_find(WIDTH * LINE_AD_X, WIDTH * (1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y)),
             9: mark_placement_pos_find(WIDTH * (1 - LINE_AD_X), WIDTH*(1 - LINE_AD_Y), HEIGHT*(1 - LINE_AD_X), HEIGHT*(1 - LINE_AD_Y))
            }

def draw_move(board, player, pos):
    if player == 'O':
        pygame.draw.circle(board, (0, 0, 0), (int(ENTRY_POS[pos][0]), int(ENTRY_POS[pos][1])), int(WIDTH/20), 1)
    elif player == 'X':
        pygame.draw.line(board, (0, 0, 0), (int(ENTRY_POS[pos][0] - 30), int(ENTRY_POS[pos][1] - 30)), \
                        (int(ENTRY_POS[pos][0] + 30), int(ENTRY_POS[pos][1] + 30)), 2)
        pygame.draw.line(board, (0, 0, 0), (int(ENTRY_POS[pos][0] + 30), int(ENTRY_POS[pos][1] - 30)), \
                        (int(ENTRY_POS[pos][0] - 30), int(ENTRY_POS[pos][1] + 30)), 2)

def minimax(grid, depth, alpha, beta, isMaximizing):
    result = check_win(grid)
    if result != None:
        return SCORE[result]
    if isMaximizing:
        bestScore = float("-inf")
        for i in range(0,3):
            for j in range(0,3):
                if grid[i][j] == '':
                    grid[i][j] = AI
                    score = minimax(grid, depth+1, alpha, beta, False)
                    grid[i][j] = ''
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break
        return bestScore
    else:
        bestScore = float("inf")
        for i in range(0,3):
            for j in range(0,3):
                if grid[i][j] == '':
                    grid[i][j] = HUMAN
                    score = minimax(grid, depth+1, alpha, beta, True)
                    grid[i][j] = ''
                    bestScore = min(bestScore, score)
                    beta = min(beta, bestScore)
                    if beta <= alpha:
                        break
        return bestScore

def Ai_move(GRID):
    if len(GRID) == 9:
        grid = transform_grid(GRID)
    else:
        grid = GRID
    bestScore = float('-inf')
    for i in range(0, 3):
        for j in range(0,3):
            if grid[i][j] == '':
                grid[i][j] = AI
                score = minimax(grid, 0, float('-inf'), float('inf'), False)
                grid[i][j] = ''
                if (score > bestScore):
                    bestScore = score
                    bestMove = [i, j]
    
    return (bestMove[0]*3)+ bestMove[1]+1

def handle_click(board, mousePos, GRID):
    global WRONG_CLICK
    global CURRENT_PLAYER
    if CURRENT_PLAYER == HUMAN:
        mouseX = mousePos[0]
        mouseY = mousePos[1]
        move = find_pos(mouseX, mouseY)
        if move == 10:
            WRONG_CLICK = True
            return 0
        else:
            WRONG_CLICK = False
            if GRID[move-1] != '':
                return 0
            GRID[move-1] = CURRENT_PLAYER
            draw_move(board, CURRENT_PLAYER, move)
            return 1
    elif CURRENT_PLAYER == AI:
        ai_pos = Ai_move(GRID)
        GRID[ai_pos - 1] = CURRENT_PLAYER
        draw_move(board, CURRENT_PLAYER, ai_pos)
        return -1


def equals(a, b, c):
    return a == b and b == c and a != ''

def transform_grid(GRID):
    if len(GRID) < 4:
        grid = ['']*9
        for i in range(0, 3):
            for j in range (0,3):
                grid[(i*3)+ j] = GRID[i][j]
    else:
        grid = [['' for i in range(3)] for j in range(3)]
        for i, val in enumerate(GRID):
            if i < len(GRID)/3:
                grid[0][i] = val
            elif i < len(GRID)*2/3:
                grid[1][i-3] = val
            else:
                grid[2][i-6] = val
    
    return grid

def check_win(GRID):
    if len(GRID) == 9:
        grid = transform_grid(GRID)
    else:
        grid = GRID
    winner = None

    #Horizontal
    for i in range(0, 3):
        if equals(grid[i][0], grid[i][1], grid[i][2]):
            winner = grid[i][0]
    
    #vertical
    for i in range(0, 3):
        if equals(grid[0][i], grid[1][i], grid[2][i]):
            winner = grid[0][i]

    #Diagonal
    if equals(grid[0][0], grid[1][1], grid[2][2]):
        winner = grid[0][0]
    elif equals(grid[2][0], grid[1][1], grid[0][2]):
        winner = grid[2][0]
    
    #open spots
    openspots = 0
    for i in range(0, 3):
        for j in range(0,3):
            if grid[i][j] == '':
                openspots += 1
    
    if winner == None and openspots == 0:
        return 'tie'
    else:
        return winner

def init_window(window):
    board = pygame.Surface(window.get_size())
    board = board.convert()
    board.fill((250, 250, 250))

    pygame.draw.line(board, (0, 0, 0), (WIDTH*LINE_AD_X, HEIGHT*LINE_AD_Y), (WIDTH*LINE_AD_X, HEIGHT*(1-LINE_AD_Y)), 2)
    pygame.draw.line(board, (0, 0, 0), (WIDTH*(1-LINE_AD_X), HEIGHT*LINE_AD_Y), (WIDTH*(1-LINE_AD_X), HEIGHT*(1-LINE_AD_Y)), 2)

    pygame.draw.line(board, (0, 0, 0), (HEIGHT*LINE_AD_Y, WIDTH*LINE_AD_X), (HEIGHT*(1-LINE_AD_Y), WIDTH*LINE_AD_X), 2)
    pygame.draw.line(board, (0, 0, 0), (HEIGHT*LINE_AD_Y, WIDTH*(1-LINE_AD_X)), (HEIGHT*(1-LINE_AD_Y), WIDTH*(1-LINE_AD_X)), 2)

    return board

def find_pos(mouseX, mouseY):
    if HEIGHT*LINE_AD_Y < mouseY < HEIGHT*LINE_AD_X:
        if WIDTH*LINE_AD_Y < mouseX < WIDTH * LINE_AD_X:
            position = 1
        elif WIDTH * LINE_AD_X < mouseX < WIDTH * (1 - LINE_AD_X):
            position = 2
        elif WIDTH * (1 - LINE_AD_X) < mouseX < WIDTH*(1 - LINE_AD_Y):
            position = 3
        else:
            position = 10
    elif HEIGHT*LINE_AD_X < mouseY < HEIGHT*(1 - LINE_AD_X):
        if WIDTH*LINE_AD_Y < mouseX < WIDTH * LINE_AD_X:
            position = 4
        elif WIDTH * LINE_AD_X < mouseX < WIDTH * (1 - LINE_AD_X):
            position = 5
        elif WIDTH * (1 - LINE_AD_X) < mouseX < WIDTH*(1 - LINE_AD_Y):
            position = 6
        else:
            position = 10
    elif HEIGHT*(1 - LINE_AD_X) < mouseY < HEIGHT*(1 - LINE_AD_Y):
        if WIDTH*LINE_AD_Y < mouseX < WIDTH * LINE_AD_X:
            position = 7
        elif WIDTH * LINE_AD_X < mouseX < WIDTH * (1 - LINE_AD_X):
            position = 8
        elif WIDTH * (1 - LINE_AD_X) < mouseX < WIDTH*(1 - LINE_AD_Y):
            position = 9
        else:
            position = 10
    else:
        position = 10
        
    return position

def game_status(status, board, color):
    pos_y = HEIGHT*(1-LINE_AD_Y) + 20
    font = pygame.font.SysFont("calibri", int(WIDTH/18))
    board.fill((250, 250, 250), (0, pos_y + 20, WIDTH, HEIGHT * LINE_AD_Y))
    text1 = font.render(status, 1, color)
    text2 = font.render(f"Your Symbol: {HUMAN}", 1, color)
    text3 = font.render(f"AI Symbol: {AI}", 1, color)
    board.blit(text1, (int(WIDTH/15), pos_y + 30))
    board.blit(text2, (int(WIDTH/15), HEIGHT/30))
    board.blit(text3, (int(WIDTH/15), HEIGHT/30 + HEIGHT/20))
    if WRONG_CLICK:
        error = font.render("Please click in correct spot!", 1, (255, 0, 0))
        board.blit(error, (int(WIDTH/15), int(HEIGHT/15)))

def display_board(window, board, status, color):
    game_status(status, board, color)
    window.blit(board, (0, 0))
    pygame.display.flip()

def menu_display_text(text, y_offset, color, text_size):
    title_font = pygame.font.SysFont("calibri", text_size)
    title_label = title_font.render(text, 1, color)
    WIN.blit(title_label, (WIDTH/2-title_label.get_width()/2, (HEIGHT/2-title_label.get_height()/2) - y_offset))

def main():
    global CURRENT_PLAYER
    global AI_FIRST
    run = True
    board = init_window(WIN)
    GRID = [''] * 9
    display_board(WIN, board, f"{CURRENT_PLAYER}'s turn", (10, 10, 10))
    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN or AI_FIRST:
                if AI_FIRST:
                    AI_FIRST = False
                if CURRENT_PLAYER == HUMAN and handle_click(board, pygame.mouse.get_pos(), GRID) == 1 and check_win(GRID) == None:
                    CURRENT_PLAYER = AI
                if CURRENT_PLAYER == AI and handle_click(board, pygame.mouse.get_pos(), GRID) == -1 and check_win(GRID) == None:
                        CURRENT_PLAYER = HUMAN
                if check_win(GRID) == "tie":
                    display_board(WIN, board, f"It's a {check_win(GRID)}", (0, 0, 250))
                    time.sleep(3)
                    return
                elif check_win(GRID) != None:
                    display_board(WIN, board, f"{check_win(GRID)} has won!", (0, 250, 0))
                    time.sleep(3)
                    return
                display_board(WIN, board, f"{CURRENT_PLAYER}'s turn", (10, 10, 10))

def who_goes_first():
    global CURRENT_PLAYER
    global AI_FIRST
    text_size = int(WIDTH/18)
    color = (100,50,50)
    run = True
    while(run):
        WIN.fill((255,255,255))
        menu_display_text("Who do you want to go first", 100, color, text_size)
        menu_display_text("AI: Press A", 50, color, text_size)
        menu_display_text("Yourself: Press H", 0, color, text_size)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                CURRENT_PLAYER = AI
                AI_FIRST = True
                main()
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                CURRENT_PLAYER = HUMAN
                AI_FIRST = False
                main()
                run = False
            elif event.type == pygame.KEYDOWN:
                menu_display_text("WRONG ENTRY!", -int(HEIGHT/8), (255,0,0), text_size)
                menu_display_text("Please either press A or H", -int(HEIGHT/6), (255,0,0), text_size)
                menu_display_text("Or Press Esc to Exit", -int(HEIGHT/4), (255,0,0), text_size)
                pygame.display.update()
                time.sleep(2)

def main_menu():
    run = True
    text_size = int(WIDTH/16)
    color = (255,255,255)
    while run:
        WIN.fill((0,0,0))
        menu_display_text("Press Enter to begin the game..", 100, color, text_size)
        menu_display_text("Or", 50, color, text_size)
        menu_display_text("Press Esc to Exit", 0, color, text_size)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                who_goes_first()
    pygame.quit()

main_menu()