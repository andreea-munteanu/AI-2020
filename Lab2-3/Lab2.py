import random
import sys
from queue import Queue

n = 20
m = 30
print("n = ", n, "m = ", m)
SIZE = (n, m)  # n rows, m columns

if sys.getrecursionlimit() < SIZE[0] * SIZE[1] :
    sys.setrecursionlimit(SIZE[0] * SIZE[1])

# if max recursion limit is lower than needed, adjust it
sys.setrecursionlimit(30000)

my_list = [0] * 70 + [1] * 30
# initializing labyrinth with 0s and 1s at weighted random
lab = list(list(random.choice(my_list) for i in range(SIZE[0])) for j in range(SIZE[1]))


def print_labyrinth() :
    print("    ", end='')
    for i in range(n):
        if i < n-1:
            print(i, end=' ')
        else:
            print(i)
    print("    ", end='')
    for i in range(2*n):
        print("_", end='')
    print('')

    for j in range(m) :
        if j < 10:
            print(j, " |", end='')
        else:
            print(j, "|", end= '')
        # print("| ", end='')
        for i in range(n) :
            if lab[j][i] == 0 :
                print(lab[j][i], end=' ')
            else :
                print('*', end=' ')
        print('|', j, end='\n')


print("\nYour labyrinth is: ")
print_labyrinth()
print("\n\n")
print("\nChoose start(xs, ys) and destination (xd, yd): ", end='')
xs, ys, xd, yd = input().split()

xs = int(xs)
ys = int(ys)
xd = int(xd)
yd = int(yd)

found = False

# (xc, yc) - current position
# (xs, ys) - start position
# (xd, yd) - destination

"""_________________________________________________________________________________________________________
                                                    1. STATE
          (xc , yc , xs , ys , xd , yd , found)
     ______________ _________ ___________ ___________________________
     current state |  start  |destination| reached final state (bool)



    _________________________________________________________________________________________________________
                              2. INITIALIZATION, INITIAL/FINAL STATE, CHECK_FINAL()

2.2. initial state: current position is start(xs, ys)
    _________________________________________________________________________________________________________
"""


# 2.1.initialization
def initialState(xc, yc, xs, ys, xd, yd, found) :
    xc = xs
    yc = ys
    found = False
    return xc, yc, xs, ys, xd, yd, found


# 2.3. bool function checking whether a state is final
def finalState(xc, yc, xd, yd) :
    return xc == xd and yc == yd


"""_________________________________________________________________________________________________________
                                            3. TRANSITION FUNCTION

    3.1. validation function (bool)
    3.2. transition function returning current state
   _________________________________________________________________________________________________________
"""


# checks if (xc, yc) is within bounds
def inside(xc, yc, n, m) :
    return 0 <= xc < n and 0 <= yc < m


visited = []


# checks if (xc, yc) has been visited before
def not_visited(xc, yc) :
    for i in range(len(visited), 2) :
        if visited[i] == xc and visited[i + 1] == yc :
            return False
    return True


# validate transition
def valid_transition(xc, yc) :
    return inside(xc, yc, n, m) and not_visited(xc, yc)


def transition(xc, yc, x_new, y_new) :
    xc = x_new
    yc = y_new
    return xc, yc


N, S, E, W = 1, 2, 4, 8

GO_DIR = {N : (0, -1),
          S : (0, 1),
          E : (1, 0),
          W : (-1, 0)}
# dictionary with directions translated to digging moves

directions = [N, E, W, S]

"""_________________________________________________________________________________________________________
                                            4. BACKTRACKING STRATEGY
   _________________________________________________________________________________________________________
"""


BKT_stack = []


def print_BKT_path(stack) :
    # stack contains indices (i,j) of the path --> requires step = 2
    for i in range(len(stack), 2) :
        # printing stack for check
        print("(", stack[i], ", ", stack[i + 1], ")", end='; ')
        # marking path with '+'
        lab[stack[i]][stack[i + 1]] = '+'
    # printing resulting path
    print("\nBKT path: ")
    print_labyrinth()
    # changing matrix to original
    for i in range(len(stack), 2) :
        lab[stack[i]][stack[i + 1]] = '0'

def BKT(xc, yc, xs, ys, xd, yd) :
    BKT_stack.append(xc)
    BKT_stack.append(yc)
    visited.append(xc)
    visited.append(yc)
    if finalState(xc, yc, xd, yd) :
        print('Found solution: ')
        print_BKT_path(BKT_stack)
        return True
    else :
        for direction in directions :
            # if transition has been made successfully, move to new position
            sum_x = [GO_DIR[direction][0], xc]
            sum_y = [GO_DIR[direction][1], yc]
            xc_new = sum(sum_x) # xc_new = GO_DIR[direction][0] + xc
            yc_new = sum(sum_y)
            if valid_transition(xc_new, yc_new) :
                new_x, new_y = transition(xc_new, yc_new, xc_new, yc_new)
                BKT(new_x, new_y, xs, ys, xd, yd)
    BKT_stack.pop()
    BKT_stack.pop()


BKT(xs, ys, xs, ys, xd, yd)

"""_________________________________________________________________________________________________________
                                            5. BFS STRATEGY
   _________________________________________________________________________________________________________
"""


class Point(object):
    def __init__(self, x, y) :
        self.x = x
        self.y = y

def BFS(xc, yc, xs, ys, xd, yd):
    q = Queue(maxsize=10000)
    position = Point(xc, yc)
    BFS_visited = set()
    BFS_visited.add(position)
    q.put(position)
    while q:
        u = q.get()
        # calculate neighbours of u, check if they are visited
        for i in range(4):
            # directions N, S, E, W
            print("new line")






