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


