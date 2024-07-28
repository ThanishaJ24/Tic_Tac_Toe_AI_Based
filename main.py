import sys
import pygame
import numpy as np

pygame.init()

# Define colors
white = (255, 255, 255)
gray = (180, 180, 180)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Set up display
width = 300
height = 300
L_width = 5
Board_row = 3
Board_col = 3
sq_size = width // Board_col
c_rad = sq_size // 3
c_width = 15
cross_width = 25

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(black)

board = np.zeros((Board_row, Board_col))

def draw_lines(color=white):
    for i in range(1, Board_row):
        pygame.draw.line(screen, color, (0, sq_size * i), (width, sq_size * i), L_width)
        pygame.draw.line(screen, color, (sq_size * i, 0), (sq_size * i, height), L_width)

def draw_fig(color=white):
    for row in range(Board_row):
        for col in range(Board_col):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col * sq_size + sq_size // 2), int(row * sq_size + sq_size // 2)), c_rad, c_width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, (col * sq_size + sq_size // 4, row * sq_size + sq_size // 4), (col * sq_size + 3 * sq_size // 4, row * sq_size + 3 * sq_size // 4), cross_width)
                pygame.draw.line(screen, color, (col * sq_size + sq_size // 4, row * sq_size + 3 * sq_size // 4), (col * sq_size + 3 * sq_size // 4, row * sq_size + sq_size // 4), cross_width)

def mark_squre(row, col, player):
    board[row][col] = player

def available_sq(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(Board_row):
        for col in range(Board_col):
            if board[row][col] == 0:
                return False
    return True

def check_win(player):
    for col in range(Board_col):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    for row in range(Board_row):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def minimax(minimax_board, depth, is_maximizing):
    if check_win(2):
        return 1
    elif check_win(1):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -1000
        for row in range(Board_row):
            for col in range(Board_col):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(Board_row):
            for col in range(Board_col):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(Board_row):
        for col in range(Board_col):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_squre(move[0], move[1], 2)
        return True
    return False

def restart_game():
    screen.fill(black)
    draw_lines()
    for row in range(Board_row):
        for col in range(Board_col):
            board[row][col] = 0

draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // sq_size
            mouseY = event.pos[1] // sq_size
            if available_sq(mouseY, mouseX):
                mark_squre(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1
                draw_fig()
                pygame.display.update()
                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1
                    draw_fig()
                    pygame.display.update()
                if not game_over and is_board_full():
                    game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1
    if game_over:
        if check_win(1):
            draw_fig(green)
            draw_lines(green)
        elif check_win(2):
            draw_fig(red)
            draw_lines(red)
        else:
            draw_fig(gray)
            draw_lines(gray)
    pygame.display.update()
