from copy import deepcopy

from Checkers import board, ROWS, COLS, turn, print_board

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

# class Piece(object):
#     def __init__(self, color, king):
#         self.color = color
#
#
# class Player(object):
#     def __init__(self, type, color):
#         self.type = type        # computer or player
#         self.color = color      # red or green
#
# def init_player(type, color):
#     return Player(type, color)


""""
________________________________________________________________
                            MOVES
________________________________________________________________
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


# check whether move within board
# works; checked
def validate_move(row, col) :
    return 0 <= row < ROWS and 0 <= col < COLS


# works; checked
def check_square_is_free(row, col) :
    return board[col][row] == 0


# determine possible moves from position pos (one level)
# works; checked
def possible_moves(pos) :
    print_board(board)
    moves = []
    x, y = pos
    # if board[x][y] == 2: # piece is computer's
    # parse all neighbours, N to NW (clockwise)
    for dirr in GO_DIR :
        print("DIR: ", dirr)
        new_x = x + GO_DIR[dirr][1]
        new_y = y + GO_DIR[dirr][0]
        print("neighbour: (", new_x, ",", new_y, ")")
        # check if neighbour within bounds:
        if validate_move(new_x, new_y) :
            # if square is free
            if check_square_is_free(new_x, new_y) :
                # move from (x, y) to (new_x, new_y)
                move = (x, y, new_x, new_y)
                moves.append(move)
        #     else :
        #         print("Direction ", dir, " is not free")
        # else :
        #     print("Direction ", dir, " is out of board")
    return moves


# pos = (2, 0)
# print(board[2][1])
# print("Possible moves: \n", *possible_moves(pos), sep='\n')

# return all possible moves for player (from all pieces)
def all_possible_moves_for_player(player):
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[col][row] == player:
                pos = (row, col)
                moves.append(possible_moves(pos))
    return moves

# from pos1 to pos2
def make_move(pos1, pos2, matrix) :
    x1, y1 = pos1
    x2, y2 = pos2
    matrix[y2][x2] = matrix[y1][x1]
    # pos1 is now free:
    matrix[y1][x1] = 0
    # square must be empty:
    # to be continued...


# best_move = [x, y, new_x, new_y] --> from (x, y) to (new_x, new_y)
best_move = []

"""
____________________________________________________________
                         FINAL STATE
____________________________________________________________
"""


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


# to be checked
def final_state() :
    # if no moves are available for players
    # or one player has placed all pieces on opposite row --> True
    moves = []
    for row in ROWS :
        for col in COLS :
            # if cell is piece:
            if not check_square_is_free(row, col) :
                pos = (row, col)
                moves.append(possible_moves(pos))
    return not moves or all_pieces_on_opposite_side() != -1


"""
_______________________________________________________________
                     EVALUATION FUNCTION
_______________________________________________________________
"""


# score of piece at position pos(x, y) on the board for player
def calc_distance(x) :
    return ROWS - x


# score for player
def score(player) :
    # player = 1 for us
    # player = 2 for computer
    player_score = 0
    for row in range(ROWS) :
        for col in range(ROWS) :
            # determine distance from initial row:
            # 1 square = 100 points
            if board[col][row] == player :
                # calculate distance from initial row
                player_score += calc_distance(row)
    return player_score


# evaluates board
def static_eval() :
    # f(n) > 0 --> advantageous for computer
    # f(n) < 0 --> advantageous for player
    # f(n) = 0 --> no one is at advantage
    ########################################
    # f(n) = score(computer) - score(player)
    return score(2) - score(1)


DEPTH_LIMIT = 3  # number of plies

"""
_______________________________________________________________
                             MINIMAX
_______________________________________________________________
"""


# uses DEPTH_LIMIT
# player = {us, computer}
def minimax(player, ply, running) :
    global best_move
    # terminal node?         are we still playing?
    # if ply >= DEPTH_LIMIT or running is False :
    #     board_score = static_eval()
    # if it's computer's turn:
    if turn == 2 :
        # initially, beta = +inf
        beta = 10000
        # determine possible moves
        available_moves = []
        for row in range(ROWS) :
            for col in range(COLS) :
                if board[col][row] == 2 :
                    pos = (row, col)
                    available_moves.append(possible_moves(pos))
        # parsing moves
        for i in range(len(available_moves)) :
            # create a deep copy of the board (otherwise pieces would be just references)
            new_board = deepcopy(board)
            make_move((available_moves[i][0], available_moves[i][1]),
                      (available_moves[i][2], available_moves[i][3]), new_board)  # make move on new board
            print_board(new_board)
            print("\n")
            ''' beta := min(beta, minimax(child, depth+1)) '''
            # switch players from 1 to 2 and vice versa
            player = 3 - player
            temp_beta = minimax(new_board, player, ply + 1)
            if temp_beta < beta :
                beta = temp_beta  # take the lowest beta
        return beta


"""
_______________________________________________________________
                             ALPHA BETA
_______________________________________________________________
"""


# def alpha_beta(player, board, ply, alpha, beta) :
#     global best_move
#
#     # find out ply depth for player
#     ply_depth = 0
#     if player != 'black' :
#         ply_depth = white.ply_depth
#     else :
#         ply_depth = black.ply_depth
#
#     end = end_game(board)
#
#     ''' if(game over in current board position) '''
#     if ply >= ply_depth or end[0] == 0 or end[1] == 0 :  # are we still playing?
#         ''' return winner '''
#         score = evaluate(board, player)  # return evaluation of board as we have reached final ply or end state
#         return score
#
#     ''' children = all legal moves for player from this board '''
#     moves = avail_moves(board, player)  # get the available moves for player
#
#     ''' if(max's turn) '''
#     if player == turn :  # if we are to play on node...
#         ''' for each child '''
#         for i in range(len(moves)) :
#             # create a deep copy of the board (otherwise pieces would be just references)
#             new_board = deepcopy(board)
#             make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board)  # make move on new board
#
#             ''' score = alpha-beta(other player,child,alpha,beta) '''
#             # ...make a switch of players for minimax...
#             if player == 'black' :
#                 player = 'white'
#             else :
#                 player = 'black'
#
#             score = alpha_beta(player, new_board, ply + 1, alpha, beta)
#
#             ''' if score > alpha then alpha = score (we have found a better best move) '''
#             if score > alpha :
#                 if ply == 0 : best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3])  # save the move
#                 alpha = score
#             ''' if alpha >= beta then return alpha (cut off) '''
#             if alpha >= beta :
#                 # if ply == 0: best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]) # save the move
#                 return alpha
#
#         ''' return alpha (this is our best move) '''
#         return alpha
#
#     else :  # the opponent is to play on this node...
#         ''' else (min's turn) '''
#         ''' for each child '''
#         for i in range(len(moves)) :
#             # create a deep copy of the board (otherwise pieces would be just references)
#             new_board = deepcopy(board)
#             make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board)  # make move on new board
#
#             ''' score = alpha-beta(other player,child,alpha,beta) '''
#             # ...make a switch of players for minimax...
#             if player == 'black' :
#                 player = 'white'
#             else :
#                 player = 'black'
#
#             score = alpha_beta(player, new_board, ply + 1, alpha, beta)
#
#             ''' if score < beta then beta = score (opponent has found a better worse move) '''
#             if score < beta : beta = score
#             ''' if alpha >= beta then return beta (cut off) '''
#             if alpha >= beta : return beta
#         ''' return beta (this is the opponent's best move) '''
#         return beta


def play_as_computer() :
    global board, DEPTH_LIMIT, turn  # global variables
    alpha = minimax(board, 1, True)
    # if there are no more moves available, print winner
    if alpha == -1000 :
        scor = static_eval()
        if scor < 0 :
            print("End of game. You win!")
        elif scor > 0 :
            print("End of game. Computer wins!")
        else :
            print("End of game. Tie.")
    else :
        # make move
        make_move(best_move[0], best_move[1], board)  # make the move on board
    # change turns
    turn = 3 - turn
