import numpy as np
import random
import itertools


def find_node(cycles, n):
    if n in cycles[0]:
        return 0, cycles[0].index(n)
    else:
        return 1, cycles[1].index(n)


def reverse(l, i, j):
    n = len(l)
    d = (j - i) % n
    for k in range(0,(abs(d) // 2) + 1):
        x1, x2 = (i + k) % n, (i + d - k) % n
        l[x1], l[x2] = l[x2], l[x1]


def is_edge_in_cycle(cycle, a, b):
    for i in range(len(cycle) - 1):
        x, y = cycle[i], cycle[1 + i]
        if (a, b) == (x, y):
            return +1
        if (a, b) == (y, x):
            return -1

    x, y = cycle[-1], cycle[0]
    if (a, b) == (x, y):
        return +1
    if (a, b) == (y, x):
        return -1

    return 0


def is_edge_in_cycle2(cycles, a, b):
    for i in [0,1]:
        status = is_edge_in_cycle(cycles[i], a, b)
        if status != 0:
            return i, status
    return None, 0


def insert_move(moves, move):
    delta_x = move[0]
    for i, x in enumerate(moves):
        delta_y = x[0]
        if delta_x < delta_y:
            moves.insert(i, move)
            return
        elif delta_x == delta_y:
            return
    moves.append(move)


def compute_delta_sn(instance, x1, y1, z1, x2, y2, z2):
    return instance[x1][y2] + instance[z1][y2] - instance[x1][y1] - instance[z1][y1] + instance[x2][y1] + instance[z2][y1] - instance[x2][y2] - instance[z2][y2]


def swap_node(instance, cycles, c1, i, c2, j):
    s_e, s_n = range(2)
    C1, C2 = cycles[c1], cycles[c2]
    n, m = len(C1), len(C2)
    x1, y1, z1 = C1[(i - 1) % n], C1[i], C1[(i + 1) % n]
    x2, y2, z2 = C2[(j - 1) % m], C2[j], C2[(j + 1) % m]
    delta = compute_delta_sn(instance, x1, y1, z1, x2, y2, z2)
    move = delta, s_n, c1, c2, x1, y1, z1, x2, y2, z2
    return delta, move


def compute_delta_se(instance, a, b, c, d):
    if a in [d,b,c] or b in [d,c] or c in [d]:
        return 1e8
    return instance[a][c] + instance[b][d] - instance[a][b] - instance[c][d]


def generate_se2(instance, cycle, i, j):
    n = len(cycle)
    nodes = cycle[i], cycle[(i + 1) % n], cycle[j], cycle[(j + 1) % n]
    return (compute_delta_se(instance, *nodes), *nodes)


def compute_delta_se2(instance, cycle, i, j):
    return generate_se2(instance, cycle, i, j)[0]


def generate_se(n):
    return [(i, (i + d) % n) for i in range(n) for d in range(2, n - 1)]


def generate_sn(n, m):
    return [(i, j) for i in range(n) for j in range(m)]


def initial_moves(instance, cycles):
    s_e, s_n = 0, 1
    moves = []
    for k in [0,1]:
        cycle = cycles[k]
        n = len(cycle)
        for i, j in generate_se(n):
            delta, a, b, c, d = generate_se2(instance, cycle, i, j)
            if delta < 0: moves.append((delta, s_e, a, b, c, d))
    for i, j in generate_sn(len(cycles[0]), len(cycles[1])):
        delta, move = swap_node(instance, cycles, 0, i, 1, j)
        if delta < 0: moves.append(move)
    return moves


def make_move(cycles, move):
    s_e, s_n = 0, 1
    type_move = move[1]
    if type_move == s_n:
        _, _, c1, c2, _, a, _, _, b, _ = move
        i, j = cycles[c1].index(a), cycles[c2].index(b)
        cycles[c1][i], cycles[c2][j] = cycles[c2][j], cycles[c1][i]
    elif type_move == s_e:
        _, _, a, _, c, _ = move
        (c1, i), (c2, j) = find_node(cycles, a), find_node(cycles, c)
        cycle = cycles[c1]
        n = len(cycle)
        reverse(cycle, (i + 1) % n, j)


def next_moves(instance, cycles, move):
    s_e, s_n = 0, 1
    type_move = move[1]
    moves = []
    if type_move == s_n:
        _, _, c1, c2, _, y1, _, _, y2, _ = move
        i, j = cycles[c1].index(y2), cycles[c2].index(y1)
        n, m = len(cycles[c1]), len(cycles[c2])
        for k in range(m):
            delta, move = swap_node(instance, cycles, c1, i, c2, k)
            if delta < 0: moves.append(move)
        for k in range(n):
            delta, move = swap_node(instance, cycles, c2, j, c1, k)
            if delta < 0:
                moves.append(move)
    elif type_move == s_e:
        _, _, a, b, c, d = move
        cycle = cycles[0] if a in cycles[0] else cycles[1]
        n = len(cycle)
        for i, j in generate_se(n):
            delta, a, b, c, d = generate_se2(instance, cycle, i, j)
            if delta < 0:
                moves.append((delta, s_e, a, b, c, d))

    return moves

