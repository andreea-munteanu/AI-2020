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
board = [[2, 2, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1]]

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
def draw_BW_board() :
    screen.fill(WHITE)
    for row in range(ROWS) :
        for col in range(row % 2, COLS, 2) :
            pygame.draw.rect(screen, BLACK, (row * SQUARE_SIZE,
                                             col * SQUARE_SIZE,
                                             SQUARE_SIZE, SQUARE_SIZE))


OUTLINE = 2
PADDING = 15
radius = SQUARE_SIZE // 2 - PADDING


# function to determine the square that we click
# NOT OKAY always returns 0 0
def getPos():
    pos = pygame.mouse.get_pos()
    col = (pos[0] - PADDING) // (WIDTH + OUTLINE)
    row = pos[1] // (HEIGHT + OUTLINE)
    return row, col

# drawing circle inside square
def drawCircle():
    # Change the x/y screen coordinates to grid coordinates
    row, col = getPos()
    # determine square and draw circle there
    pygame.draw.circle(screen, RED, (row, col), 20)


# draw green and red pieces
def draw_pieces() :
    for row in range(ROWS):
        for col in range(COLS) :
            # get coordinates
            x, y = row * SQUARE_SIZE, col * SQUARE_SIZE - PADDING
            # red for opponent
            if board[row][col] == 2:
                pygame.draw.circle(screen, RED, (y + radius + 2 * PADDING + OUTLINE, x + radius + PADDING + OUTLINE), radius)
                # # green for player
                # pygame.draw.circle(screen, GREEN, (ROWS - 1, col), radius, radius + OUTLINE)
                xCoordinate = ((OUTLINE + WIDTH) * row + OUTLINE + 32) + PADDING
                yCoordinate = (OUTLINE + HEIGHT) * col + OUTLINE + 33
            # green for player
            elif board[row][col] == 1 :
                pygame.draw.circle(screen, GREEN, (y + radius + 2*PADDING + OUTLINE, x + radius + PADDING + OUTLINE), radius)
                # Draw a white outline around edge of black pieces so they are visible
                # when placed on black game board squares.
                # pygame.draw.circle(screen, RED, (xCoordinate, yCoordinate), radius, 1)
            # empty square - do nothing
            else:
                continue



# def create_board(self):
#     for row in range(ROWS):
#         self.board.append([])
#         for col in range(COLS):
#             if col % 2 == ((row + 1) % 2):
#                 if row == 0:
#                     self.board[row].append(Piece(row, col, GREEN))
#                 elif row == 4:
#                     self.board[row].append(Piece(row, col, RED))
#                 else:
#                     self.board[row].append(0)
#             else:
#                 self.board[row].append(0)


# def minimax():
#     def simulate_move(piece, move, board, game, skip):
#         board.move(piece, move[0], move[1])
#         if skip:
#             board.remove(skip)
#         return board
#
#     def get_possible_moves(position, color, game):
#         moves = [[board, piece]]
#         for piece in board.get_all_pieces(color):
#             valid_moves = board.get_valid_moves(piece)
#             (row, col): [pieces]
#             for move, skip in valid_moves.items():
#                 temp_board = deepcopy(board)
#                 new_board = simulate_move(piece, move, temp_board, game, skip)
#                 moves.append([new_board, piece])
#         return moves
#
#     if max_player:
#         max_eval = float('-inf')
#         optimal_move = None
#         for move in get_possible_moves():


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
                drawCircle()
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()


main()
