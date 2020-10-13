import random
import sys

# (xc, yc) - current position
# (xs, ys) - start position
# (xd, yd) - destination

N, S, E, W = 1, 2, 4, 8
# directions translated into bitnums to store information on all cleared walls in one variable per cell

GO_DIR = {N : (0, -1), S : (0, 1), E : (1, 0), W : (-1, 0)}
# dictionary with directions translated to digging moves

REVERSE = {E : W, W : E, N : S, S : N}
# when a passage is dug from a cell, the other cell obtains the reverse passage, too

directions = [N, E, W, S]


# creating labyrinth n x m
def createLabyrinth(n, m) :
    SIZE = (int(n), int(m)) # n rows, m columns
    # size of the labyrinth (x, y)

    if sys.getrecursionlimit() < SIZE[0] * SIZE[1] :
        sys.setrecursionlimit(SIZE[0] * SIZE[1])
    # if max recursion limit is lower than needed, adjust it

    lab = list(list(0 for i in range(SIZE[0])) for j in range(SIZE[1]))

    # labyrinth is prepared
    def dig(x, y) :
        # digs passage from a cell (x, y) in an unvisited cell
        dirs = [N, E, W, S]
        random.shuffle(dirs)
        # shuffles directions each time for more randomness
        for dir in dirs :
            new_x = x + GO_DIR[dir][0]
            new_y = y + GO_DIR[dir][1]
            if (new_y in range(SIZE[1])) and \
                    (new_x in range(SIZE[0])) and \
                    (lab[new_y][new_x] == 0) :
                # checks if the new cell is not visited
                lab[y][x] |= dir
                lab[new_y][new_x] |= REVERSE[dir]
                # if so, apply info on passages to both cells
                dig(new_x, new_y)
                # repeat recursively

    def check() :
        # displays the cells' values for check-up
        for i in range(SIZE[1]) :
            for j in range(SIZE[0]) :
                print(" " * (1 - (lab[i][j] // 10)) + \
                      str(lab[i][j]), end='|')
            print('')

    def draw() :
        # displays the labyrinth
        print("\nLabyrinth of Kuba #" + str(seed) + " (" + str(SIZE[0]) + "x" + str(SIZE[1]) + ")")
        # prints the seed (for reference) and the lab size
        print("_" * (SIZE[0] * 2))
        for j in range(SIZE[1]) :
            if j != 0 :
                print("|", end='')
            else :
                print("_", end='')
            for i in range(SIZE[0]) :
                if lab[j][i] & S != 0 :
                    print(" ", end='')
                else :
                    print("_", end='')
                if lab[j][i] & E != 0 :
                    if (lab[j][i] | lab[j][i + 1]) & S != 0 :
                        print(" ", end='')
                    else :
                        print("_", end='')
                elif (j == SIZE[1] - 1) & (i == SIZE[0] - 1) :
                    print("_", end='')
                else :
                    print("|", end='')
            print("")

    # Let's start!
    seed = random.randint(0, 1000)
    random.seed(seed)
    dig(SIZE[0] // 2, SIZE[1] // 2)
    draw()
    # check()


# states: (matrix, n, m, xc, yc, xs, ys, xd, yd)

# make current = start
def initialState(lab, n, m, xc, yc, xs, ys, xd, yd) :
    xc = yc
    yc = ys


# current = destination
def finalState(lab, n, m, xc, yc, xs, ys, xd, yd) :
    return bool(xc == xd and yc == yd)


# checks whether we can move from current position (xc, yc) to direction dir:
# dir can be N = 1, S = 2, E = 4, W = 8
def inside(lab, n, m, xc, yc, xs, ys, xd, yd) :
    return bool(0 <= xc < n and 0 <= yc < m)

# checks if (xc, yc) has been visited before
def isFree(lab, n, m, xc, yc, xs, ys, xd, yd) :
    return lab[xc][yc] == 0

# transitioning from current position (xc, yc) to N / E / S / W by 1 position (if possible)
def transition(lab, n, m, xc, yc, xs, ys, xd, yd, dir) :
    # calculate new coordinates
    new_x = xc + GO_DIR[dir][0]
    new_y = yc + GO_DIR[dir][1]
    if inside(lab, n, m, new_x, new_y, xs, ys, xd, yd) :
        # checks if the new cell is not visited
        lab[yc][xc] |= dir
        lab[new_y][new_x] |= REVERSE[dir]


def BKT(lab, n, m, xc, yc, xs, ys, xd, yd, dir) :
    lab[xc][yc] |= dir


""" void BKT(int x, int y, int k)
{
    int xv,yv;
    st[k].x=x;
    st[k].y=y;
    a[x][y]=1; ///se marcheaza punctul
    if (x==xc && y==yc) afis(k);
    else for (int i=0; i<=3; ++i)
    {
        ///se calculeaza vecinii
        xv=x+dx[i];
        yv=y+dy[i];
        ///daca vecinii sunt nemarcati pe harta (adica drumul e liber), soricelul se deplaseaza cu o pozitie in sensul acelor de ceasornic (N,E,S,V)
        if (interior(xv,yv) && a[xv][yv]==0) BKT(xv,yv,k+1);
    }
    a[x][y]=0; ///operatia complementara
}
"""


def BFS(lab, n, m, xc, yc, xs, ys, xd, yd) :
    print("None =) ")

def HillClimbing(lab, n, m, xc, yc, xs, ys, xd, yd):
    print('none =)')


def main() :
    print("Input: n, m, start(xs, ys), desination(xd, yd): ")
    n, m, xs, ys, xd, yd = input().split()
    lab = None
    createLabyrinth(n, m)
    initialState(lab, n, m, xs, ys, xs, ys, xd, yd)


if __name__ == "__main__" :
    main()
