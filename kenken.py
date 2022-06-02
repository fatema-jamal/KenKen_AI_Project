from random import shuffle, randint, choice, random
from functools import reduce
from itertools import product, permutations
from sys import stderr, stdin
import csp

def adjacent(xy_first, xy_second):
    x1, y1 = xy_first
    x2, y2 = xy_second
    delta_x, delta_y = x1 - x2, y1 - y2
    return (delta_x == 0 and abs(delta_y) == 1) or (delta_y == 0 and abs(delta_x) == 1)

# convert operation from string format 
def operation(op):
    if op == '+':
        return lambda a, b: a + b
    elif op == '-':
        return lambda a, b: a - b
    elif op == '*':
        return lambda a, b: a * b
    elif op == '/':
        return lambda a, b: a / b
    else:
        return None
def generate(size):  
    #filling array in order
    board1= [[0 for x in range(size)] for y in range(size)]
    
    for i in range(size):
        for j in range(size):
            board1[i][j]= ((i + j) % size) + 1
    #shuffling board's rows
    for k in range(size):
        shuffle(board1)
    #shuffling board's columns 
    for c1 in range(size):
        for c2 in range(size):
            if random() > 0.4:
                for r in range(size):
                    board1[r][c1], board1[r][c2] = board1[r][c2], board1[r][c1]

    board={}
    for i in range(size):
        for j in range(size):
            board[(j+1, i+1)]= board1[i][j]
    print('board',board)
    #initialize uncaged with all coordiantes
    uncaged = sorted(board.keys(), key=lambda var: var[1])
    cages = []
    while uncaged:
        cages.append([])
        #max size of cells in cage = 4
        cage_size = randint(1, 4)
        cell = uncaged[0]
        uncaged.remove(cell)
        cages[-1].append(cell)

        for m in range(cage_size - 1):
            adjs=[]
            for other in uncaged:
                if(adjacent(cell, other)):
                    adjs.append(other)
            if adjs:
                cell = choice(adjs)
            else: 
                cell = None
    
            if not cell:
                break

            uncaged.remove(cell)

            cages[-1].append(cell)

        cage_size = len(cages[-1])
        if cage_size == 1:
            cell = cages[-1][0]
            cages[-1] = ((cell, ), '.', board[cell])
            continue
        elif cage_size == 2:
            fst, snd = cages[-1][0], cages[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                operator = "/" # choice("+-*/")
            else:
                operator = "-" # choice("+-*")
        else:
            operator = choice("+*")
        target = reduce(operation(operator), [board[cell] for cell in cages[-1]])
        cages[-1] = (tuple(cages[-1]), operator, int(target))

    return size, cages

def get_domains(size, cages):
    domains = {}
    def qualifies(values):
        return not conflicting(members, values, members, values) and satisfies(values, operation(operator), target)

    for cage in cages:
        members, operator, target = cage
        domains[members] = list(product(range(1, size + 1), repeat=len(members)))
        domains[members] = list(filter(qualifies, domains[members]))

    return domains

def get_neighbours(cages):
    neighbors = {}
    for members, _, _ in cages:
        neighbors[members] = []

    for A, _, _ in cages:
        for B, _, _ in cages:
            if A != B and B not in neighbors[A]:
                if conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                    neighbors[A].append(B)
                    neighbors[B].append(A)

    return neighbors

#check if two cells in same rows or columns have the same value
def conflicting(A, a, B, b):
    for i in range(len(A)):
        for j in range(len(B)):
            if (A[i][0] == B[j][0]) != (A[i][1] == B[j][1]) and a[i] == b[j]:
                return True
    return False

def satisfies(values, operation, target):
    for p in permutations(values):
        if reduce(operation, p) == target:
            return True
    return False

class Kenken(csp.CSP):
    
    def __init__(self, size, cages):

        #get cells
        variables=[]
        for members,_, _ in cages:
            variables.append(members)
        #get domains
        domains = get_domains(size, cages)

        neighbors = get_neighbours(cages)

        csp.CSP.__init__(self, variables, domains, neighbors, self.constraint)

        self.size = size




    def constraint(self, A, a, B, b):
        self.checks += 1

        return A == B or not conflicting(A, a, B, b)


       
if __name__ == "__main__":
    size1,test = generate(6)

    ken3 = Kenken(size1, test)
    assignment3 = csp.backtracking_search(ken3, inference=csp.mac)
  
