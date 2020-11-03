import pygame
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

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # window dimensions
pygame.display.set_caption('Simple Checkers')       # title
icon = pygame.image.load('board.png')               # icon
pygame.display.set_icon(icon)
# initially, all pieces are placed on rows 0 and 3
board = [[2, 2, 2, 2],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1]] # --> initial state

OUTLINE = 2
PADDING = 15
radius = SQUARE_SIZE // 2 - PADDING   # radius = 47
# Board is:
#
# 2 2 2 2 ----> red (compuuter)
# 0 0 0 0
# 0 0 0 0
# 1 1 1 1 ----> green (player)

def print_board(matrix):
    for row in range(ROWS):
        for col in range(COLS):
            print(matrix[row][col], end=' ')
        print('', end='\n')

# print_board(board)

# draw B&W board
def draw_BW_board() : # works
    screen.fill(WHITE)
    for row in range(ROWS) :
        for col in range(row % 2, COLS, 2) :
            pygame.draw.rect(screen, BLACK, (row * SQUARE_SIZE,
                                             col * SQUARE_SIZE,
                                             SQUARE_SIZE, SQUARE_SIZE))


# draw green and red pieces
def draw_pieces() : # works
    for row in range(ROWS):
        for col in range(COLS) :
            # get coordinates
            x, y = row * SQUARE_SIZE, col * SQUARE_SIZE - PADDING
            # red for opponent
            if board[row][col] == 2:
                pygame.draw.circle(screen, RED, (y + radius + 2 * PADDING + OUTLINE, x + radius + PADDING + OUTLINE), radius)
                # xCoordinate = ((OUTLINE + WIDTH) * row + OUTLINE + 32) + PADDING
                # yCoordinate = (OUTLINE + HEIGHT) * col + OUTLINE + 33
            # green for player
            elif board[row][col] == 1 :
                pygame.draw.circle(screen, GREEN, (y + radius + 2*PADDING + OUTLINE, x + radius + PADDING + OUTLINE), radius)
            # empty square - do nothing
            else:
                continue


# function to determine the square that we click
# NOT OKAY always returns 0 0
def getPos():
    pos = pygame.mouse.get_pos()
    col = (pos[0] - PADDING) // (WIDTH + OUTLINE)
    row = pos[1] // (HEIGHT + OUTLINE)
    return row, col

# should work
def getColor(pos):
    x = pos[0]
    y = pos[1]
    if board[x][y] == 1:
        return GREEN
    elif board[x][y] == 2:
        return RED

# drawing circle inside square
def drawCircle(pos):
    # Change the x/y screen coordinates to grid coordinates
    color = getColor(pos)
    # determine square and draw circle there
    pygame.draw.circle(screen, color, (pos[0] + radius + 2 * PADDING + OUTLINE, pos[1] + radius + PADDING + OUTLINE), radius)


def get_piece(row, col) :
    return board[row][col]


def calc_pos(row, col) :
    x = SQUARE_SIZE * col + SQUARE_SIZE // 2
    y = SQUARE_SIZE * row + SQUARE_SIZE // 2
    return x, y


def updatePoint():
    print("updating points")


FPS = 60

def main() :
    draw_BW_board()
    draw_pieces()
    running = True
    # clock = pygame.time.Clock()
    while running :
        # clock.tick(FPS)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN :
                pos = getPos() # pos[0][1]
                drawCircle(pos)
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()


main()
