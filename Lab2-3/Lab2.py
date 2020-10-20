import random
import sys
from queue import Queue

n = 12
m = 15
print("n = ", n, "m = ", m)
SIZE = (n, m)  # n rows, m columns

if sys.getrecursionlimit() < SIZE[0] * SIZE[1] :
    sys.setrecursionlimit(SIZE[0] * SIZE[1])

# if max recursion limit is lower than needed, adjust it
sys.setrecursionlimit(30000)

my_list = [0] * 55 + [1] * 45  # weights
# initializing labyrinth with 0s and 1s at weighted random
lab = list(list(random.choice(my_list) for i in range(SIZE[0])) for j in range(SIZE[1]))


# parameters: start, destination
def print_labyrinth(xs, ys, xd, yd) :
    print("    ", end='')
    for i in range(n) :
        if i < n - 1 :
            print(i, end=' ')
        else :
            print(i)
    print("    ", end='')
    for i in range(2 * n) :
        print("_", end='')
    print('')

    for j in range(m) :
        if j < 10 :
            print(j, " |", end='')
        else :
            print(j, "|", end='')
        # print("| ", end='')
        for i in range(n) :
            # start position
            if i == xs and j == ys :
                print('S', end=' ')
            # destination
            elif i == xd and j == yd :
                print('D', end=' ')
            # free cell
            elif lab[j][i] == 0 :
                print(' ', end=' ')
            # obstacle
            else :
                print('∎', end=' ')
        print('|', j, end='\n')


"""_________________________________________________________________________________________________________
                                                    1. STATE
          (xc , yc , xs , ys , xd , yd)
     ______________ _________ ___________ 
     current state |  start  |destination| 
    
    # (xc, yc) - current position
    # (xs, ys) - start position
    # (xd, yd) - destination

    _________________________________________________________________________________________________________
                              2. INITIALIZATION, INITIAL/FINAL STATE, CHECK_FINAL()

2.2. initial state: current position is start(xs, ys)
    _________________________________________________________________________________________________________
"""


# 2.1.initialization + returning state
def initialState(xc, yc, xs, ys, xd, yd) :
    xc = xs
    yc = ys
    return xc, yc, xs, ys, xd, yd


# 2.3. bool function checking whether a state is final
def finalState(xc, yc, xd, yd) :
    return xc == xd and yc == yd


"""_________________________________________________________________________________________________________
                                            3. TRANSITION FUNCTION
                                            
    3.1. validation function (bool)
    3.2. transition function returning current state
   _________________________________________________________________________________________________________
"""

visited = []


# checks if (xc, yc) is within bounds
def inside(x, y) :
    return 0 <= x < n and 0 <= y < m


# checks if (xc, yc) has been visited before: visited = False, not visited = true
def not_visited(x, y) :
    for i in range(0, len(visited), 2) :
        if visited[i] == x and visited[i + 1] == y :
            return False
    return True


def is_obstacle(x, y) :
    if 0 <= x < n and 0 <= y < m:
        return lab[x][y] == 1
    else:
        return True


# validate transition
def valid_transition(x, y) :
    return inside(x, y) and not_visited(x, y) and is_obstacle(x, y) == False

def valid_transition_for_bkt(x,y):
    if inside(x, y):
        return is_obstacle(x, y) == False
    return False

# TRANSITION FUNCTION (returns new state)
def transition(x_new, y_new, xs, ys, xd, yd) :
    xc = x_new
    yc = y_new
    # current position (xc, yc) becomes (x_new, y_new)
    return xc, yc, xs, ys, xd, yd


N, S, E, W = 1, 2, 4, 8

GO_DIR = {N : (0, -1),
          S : (0, 1),
          E : (1, 0),
          W : (-1, 0)}
# dictionary with directions translated to digging moves

directions = [N, E, S, W]

"""_________________________________________________________________________________________________________
                                            4. BACKTRACKING STRATEGY
   _________________________________________________________________________________________________________
"""

BKT_stack = []


def print_BKT_path(xs, ys, xd, yd, stack) :
    # stack contains indices (i,j) of the path --> requires step = 2
    for i in range(0, len(stack), 2) :
        # printing stack for check
        print("(", stack[i], ", ", stack[i + 1], ")", end='; ')
        lab[stack[i]][stack[i + 1]] = 1
    # printing resulting path
    print("\nBKT path: ")
    print_labyrinth(xs, ys, xd, yd)
    # changing matrix to original
    for i in range(0, len(stack), 2) :
        lab[stack[i]][stack[i + 1]] = 0


def BKT(xc, yc, xs, ys, xd, yd) :
    # add current position to stack
    # BKT_stack.append(xc)
    # BKT_stack.append(yc)
    # # mark cell as visited
    # visited.append(xc)
    # visited.append(yc)
    lab[xc][yc] = 1
    # check if current state is final
    if finalState(xc, yc, xd, yd) :
        print('Found solution: ')
        print_BKT_path(xs, ys, xd, yd, BKT_stack)
        return True
    # check the neighbouring cells
    else :
        for direction in directions :  # N, E, W, S
            # if transition has been made successfully, move to new position
            sum_x = [GO_DIR[direction][1], xc]
            sum_y = [GO_DIR[direction][0], yc]

            # neighbour coordinates:
            xc_new = sum(sum_x)
            yc_new = sum(sum_y)

            # if transition can be done, perform
            if valid_transition_for_bkt(xc_new, yc_new) :
                new_x, new_y, xs, ys, xd, yd = transition(xc_new, yc_new, xs, ys, xd, yd)
                print("X: " , new_x , " ,Y: " , new_y)
                if BKT(new_x, new_y, xs, ys, xd, yd):
                    return True
    # complementary operations
    lab[xc][yc] = 0
    # BKT_stack.pop()
    # BKT_stack.pop()
    # visited.pop()
    # visited.pop()


"""_________________________________________________________________________________________________________
                                            5. BFS STRATEGY
   _________________________________________________________________________________________________________
"""


class Point(object) :
    def __init__(self, x, y) :
        self.x = x
        self.y = y


def BFS(xc, yc, xs, ys, xd, yd) :
    q = Queue(maxsize=10000)
    current_position = Point(xc, yc)
    BFS_visited = set()
    BFS_visited.add(current_position)
    q.put(current_position)
    while q :
        u = q.get()
        # calculate neighbours of u, check if they are visited
        for dir in directions :
            # directions N, S, E, W
            sum_x = [GO_DIR[dir][1], u.x]
            sum_y = [GO_DIR[dir][0], u.y]
            # neighbour coordinates:
            x_neigh = sum(sum_x)
            y_neigh = sum(sum_y)
            neighbour = Point(x_neigh, y_neigh)
            list_queue = list(q.queue)
            if neighbour not in list_queue :
                BFS_visited.add(neighbour)
                q.put(neighbour)
    return BFS_visited


def print_BFS_path(xs, ys, xd, yd, BFS_visited) :
    # BFS_visited() is a set containing the visited cells (in order)
    initial_set = set()
    for i in range(len(BFS_visited)) :
        v = BFS_visited.pop()
        initial_set.add(v)
        lab[v.y][v.x] = 1
    # printing resulting path
    print("\nBFS path: ")
    print_labyrinth(xs, ys, xd, yd)
    # changing matrix to original
    for i in range(len(initial_set)) :
        v = initial_set.pop()
        lab[v.y][v.x] = 0


"""_________________________________________________________________________________________________________
                                            5. HILLCLIMBING STRATEGY
   _________________________________________________________________________________________________________
"""


def HillClimbing(xc, yc, xs, ys, xd, yd) :
    print('nothing here :) ')


def main() :
    print("\nChoose start(xs, ys) and destination (xd, yd): ", end='')
    # xs, ys, xd, yd = input().split()
    xs = input()
    xs = int(xs)
    ys = input()
    ys = int(ys)
    xd = input()
    xd = int(xd)
    yd = input()
    yd = int(yd)
    print("\nYour labyrinth is: ")
    print_labyrinth(xs, ys, xd, yd)
    # BKT
    if not BKT(xs, ys, xs, ys, xd, yd):
        print("nu am gasit solutie")
    # BFS
    # BFS(xs, ys, xs, ys, xd, yd)
    # BFS_set = BFS(xs, ys, xs, ys, xd, yd)
    # print_BFS_path(xs, ys, xd, yd, BFS_set)


if __name__ == "__main__" :
    main()
