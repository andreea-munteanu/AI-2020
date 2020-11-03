from Checkers import board, ROWS, COLS, print_board

"""
___________________________________________________________
                     INITIAL STATE
____________________________________________________________
Board is:

2 2 2 2 ----> red (compuuter)
0 0 0 0
0 0 0 0
1 1 1 1 ----> green (player)
"""

N, NE, E, SE, S, SW, W, NW = 0, 1, 2, 3, 4, 5, 6, 7

direction = [N, NE, E, SE, S, SW, W, NW]

GO_DIR = {N : (-1, 0),
          NE : (-1, 1),
          E : (0, 1),
          SE : (1, 1),
          S : (1, 0),
          SW : (1, -1),
          W : (0, -1),
          NW : (-1, -1)}

# works; checked
def check_square_is_free(row, col) :
    return board[col][row] == 0


# check whether move within board
# works; checked
def validate_move(row, col) :
    return 0 <= row < ROWS and 0 <= col < COLS


# determine possible moves from position pos
# works; checked
def possible_moves(pos) :
    print_board(board)
    moves = []
    x, y = pos
    # if board[x][y] == 2: # piece is computer's
    # parse all neighbours, N to NW (clockwise)
    for dir in GO_DIR :
        print("DIR: ", dir)
        new_x = x + GO_DIR[dir][1]
        new_y = y + GO_DIR[dir][0]
        print("neighbour: (", new_x, ",", new_y, ")")
        # check if neighbour within bounds:
        if validate_move(new_x, new_y) :
            # if square is free
            if check_square_is_free(new_x, new_y) :
                move = (x, y, "-->", new_x, new_y)
                moves.append(move)
        #     else :
        #         print("Direction ", dir, " is not free")
        # else :
        #     print("Direction ", dir, " is out of board")
    return moves


"""
____________________________________________________________
                         FINAL STATE
____________________________________________________________
"""

# to be checked
def final_state():
    # if no moves are available for players
    # or one player has placed all pieces on opposite row --> True
    moves = []
    for row in ROWS:
        for col in COLS:
            # if cell is piece:
            if not check_square_is_free(row, col):
                pos = (row, col)
                moves.append(possible_moves(pos))
    return not moves or all_pieces_on_opposite_side() is not -1


# pos = (2, 0)
# print(board[2][1])
# print("Possible moves: \n", *possible_moves(pos), sep='\n')

"""
_______________________________________________________________
                     EVALUATION FUNCTION
_______________________________________________________________
"""


def eval_function(move) :
    print("yeah idk")

# works; checked
def all_pieces_on_opposite_side() :
    # returns 2 if computer wins
    # returns 1 if player wins
    # returs -1 if there is no final position
    print_board(board)
    print('\n')
    computer = 0
    player = 0
    for col in range(0, COLS) :
        # merge pe linia 0
        if board[0][col] == 1 :
            # print(0, col)
            player += 1
        # merge pe linia 3
        if board[3][col] == 2 :
            computer += 1
    if computer == ROWS :
        print("Computer wins the game")
        return 2
    elif player == ROWS :
        print("Player wins the game")
        return 1
    return -1


# print(all_pieces_on_opposite_side())


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


DEPTH_LIMIT = 3  # number of plies

def minimax(pos) :
    x, y = pos
