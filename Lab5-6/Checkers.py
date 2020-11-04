import pygame
from pygame import font
import Algorithm

import os

# os.startfile(r"D:\Facultate\Anul_3\AI\Lab 5-6\Exemplu\SimpleCheckers.exe")

# INITIALIZE GAME
pygame.init()

WIDTH, HEIGHT = 500, 500
ROWS, COLS = 4, 4
SQUARE_SIZE = WIDTH // ROWS

# RGB
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # window dimensions
pygame.display.set_caption('Simple Checkers')  # title
icon = pygame.image.load('board.png')  # icon
pygame.display.set_icon(icon)

# initially, all pieces are placed on rows 0 and 3
board = [[2, 2, 2, 2],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1]]  # --> initial state

# Board is:
#
# 2 2 2 2 ----> red (compuuter)
# 0 0 0 0
# 0 0 0 0
# 1 1 1 1 ----> green (player)

OUTLINE = 2
PADDING = 15
radius = SQUARE_SIZE // 2 - PADDING  # radius = 47

# whose turn it is to play: 1 - player, 2 - computer
turn = 2
selected = (0, 0)


def print_board(matrix) :
    for row in range(ROWS) :
        for col in range(COLS) :
            print(matrix[row][col], end=' ')
        print('', end='\n')


# print_board(board)

# draw B&W board
def draw_BW_board() :  # works
    screen.fill(WHITE)
    for row in range(ROWS) :
        for col in range(row % 2, COLS, 2) :
            pygame.draw.rect(screen, BLACK, (row * SQUARE_SIZE,
                                             col * SQUARE_SIZE,
                                             SQUARE_SIZE, SQUARE_SIZE))


# works; checked
def draw_piece(row, column, color) :
    # center_pixel(poxX, posY)
    posY = ((WIDTH / 8) * column) - (WIDTH / 8) / 2
    posX = ((HEIGHT / 8) * row) - (HEIGHT / 8) / 2
    pygame.draw.circle(screen, color, (posX, posY), 12)  # draw piece border
    pygame.draw.circle(screen, color, (posX, posY), 10)  # draw piece


# draw green and red pieces
def draw_pieces() :  # works
    for row in range(ROWS) :
        for col in range(COLS) :
            # get coordinates
            x, y = row * SQUARE_SIZE, \
                   col * SQUARE_SIZE - PADDING
            # red for opponent
            if board[row][col] == 2 :
                pygame.draw.circle(screen, RED, (y + radius + 2 * PADDING + OUTLINE, x + radius + PADDING + OUTLINE),
                                   radius)
                # xCoordinate = ((OUTLINE + WIDTH) * row + OUTLINE + 32) + PADDING
                # yCoordinate = (OUTLINE + HEIGHT) * col + OUTLINE + 33
            # green for player
            elif board[row][col] == 1 :
                pygame.draw.circle(screen, GREEN, (y + radius + 2 * PADDING + OUTLINE, x + radius + PADDING + OUTLINE),
                                   radius)
            # empty square - do nothing
            else :
                continue


def draw() :
    draw_BW_board()
    draw_pieces()


# should work
def getColor(pos) :
    x = pos[0]
    y = pos[1]
    if board[x][y] == 1 :
        return GREEN
    elif board[x][y] == 2 :
        return RED


# drawing circle inside square
def drawCircle(pos) :
    # Change the x/y screen coordinates to grid coordinates
    color = getColor(pos)
    # determine square and draw circle there
    pygame.draw.circle(screen, color, (pos[0] + radius + 2 * PADDING + OUTLINE, pos[1] + radius + PADDING + OUTLINE),
                       radius)


# showing message for user on screen
def show_message(message) :
    text = font.render(' ' + message + ' ', True, (255, 255, 255), (120, 195, 46))  # create message
    textRect = text.get_rect()  # create a rectangle
    textRect.centerx = screen.get_rect().centerx  # center the rectangle
    textRect.centery = screen.get_rect().centery
    screen.blit(text, textRect)  # blit the text


# function displaying position of clicked square
def mouse_click(pos) :
    global selected, turn
    column = pos[0] \
        # /(window_size[0]/board_size)
    row = pos[1] \
        # /(window_size[1]/board_size)
    if board[row][column] != 0 and board[row][column].color == turn :
        selected = row, column  # 'select' a piece
    else :
        moves = Algorithm.all_possible_moves_for_player(2)  # get available moves for computer
        for i in range(len(moves)) :
            if selected[0] == moves[i][0] and selected[1] == moves[i][1] :
                if row == moves[i][2] and column == moves[i][3] :
                    Algorithm.make_move(selected, (row, column), board)  # make the move
                    turn = 3 - turn


FPS = 60


def main() :
    draw()
    running = True
    clock = pygame.time.Clock()
    while running :
        clock.tick(FPS)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == left :
                mouse_click(event.pos)  # mouse click

        # let user know what's happening (whose turn it is)
        # create antialiased font, color, background
        if turn == 1 :
            show_message('YOUR TURN')
        else :
            show_message('COMPUTER THINKING...')
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()


main()
