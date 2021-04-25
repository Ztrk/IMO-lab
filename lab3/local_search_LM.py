import numpy as np
import random
import itertools
from algorithm import Algorithm
from solution import Solution
from typing import List, Tuple, Set
from lab3.helpers import *


class LocalSearchLM(Algorithm):
    def __init__(self, starting_solution):
        self.starting_solution = starting_solution


    def run(self, instance: List[List[int]], start_num: int) -> Solution:
        s_e, s_n = 0, 1
        cycles = self.starting_solution.run(instance, start_num).cycles
        lm = sorted(initial_moves(instance, cycles), key=lambda x: x[0])

        while True:
            to_delete = []
            best_move = None
            for k, move in enumerate(lm):
                type_move = move[1]
                if type_move == s_e:
                    _, _, a, b, c, d = move
                    c1, s1 = is_edge_in_cycle2(cycles, a, b)
                    c2, s2 = is_edge_in_cycle2(cycles, c, d)
                    if c1 != c2 or s1 == 0 or s2 == 0:
                        to_delete.append(k)
                    elif s1 == s2 == +1:
                        to_delete.append(k)
                        best_move = move
                        break
                    elif s1 == s2 == -1:
                        to_delete.append(k)
                        best_move = move[0], s_e, b, a, d, c
                        break
                elif type_move == s_n:
                    _, _, c1, c2, x1, y1, z1, x2, y2, z2 = move
                    s1 = is_edge_in_cycle(cycles[c1], x1, y1)
                    s2 = is_edge_in_cycle(cycles[c1], y1, z1)
                    s3 = is_edge_in_cycle(cycles[c2], x2, y2)
                    s4 = is_edge_in_cycle(cycles[c2], y2, z2)

                    if c1 == c2 or s1 == 0 or s2 == 0 or s3 == 0 or s4 == 0:
                        to_delete.append(k)
                    elif s1 == s2 and s3 == s4:
                        to_delete.append(k)
                        best_move = move
                        break

            if best_move is None:
                break

            for i in reversed(to_delete):
                del (lm[i])

            make_move(cycles, best_move)

            new_lm = next_moves(instance, cycles, best_move)
            lm = sorted(list(set(lm).union(set(new_lm))), key=lambda x: x[0])

        return Solution(cycles, instance)