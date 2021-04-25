from algorithm import Algorithm
from solution import Solution
from typing import List, Tuple, Set
from lab3.helpers import *


class LocalSearchCM(Algorithm):
    def __init__(self, starting_solution):
        self.starting_solution = starting_solution

    def run(self, instance: List[List[int]], start_num: int) -> Solution:
        k = 8
        n = len(instance)
        cycles = self.starting_solution.run(instance, start_num).cycles
        closest = np.argpartition(instance, k + 1, axis=1)[:, :k + 1]

        s_e, s_n = 0, 1
        while True:
            best_move, best_delta = None, 0
            for a in range(0,n):
                for b in closest[a]:
                    if a == b:
                        continue
                    #print(cycles)
                    (c1, i), (c2, j) = find_node(cycles, a), find_node(cycles, b)
                    move, delta = None, None
                    if c1 == c2:
                        cycle = cycles[c1]
                        c = len(cycle)
                        a1, b1, a2, b2 = a, cycle[(i + 1) % c], b, cycle[(j + 1) % c]
                        delta = compute_delta_se(instance, a1, b1, a2, b2)
                        move = delta, s_e, a1, b1, a2, b2
                    else:
                        delta, move = swap_node(instance, cycles, c1, i, c2, j)

                    if delta < best_delta:
                        best_delta = delta
                        best_move = move

            if best_move is None:
                break

            make_move(cycles, best_move)

        return Solution(cycles, instance)

