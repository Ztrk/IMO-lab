from algorithm import Algorithm
from solution import Solution
from typing import List, Tuple, Set
import random
from lab4.local_search import LocalSearch
from lab4.neighborhood import edge_swap_neighborhood, range_random_start, neighbor_vertices, compute_delta
from lab4.randomized_cycle_heuristic import RandomizedCycleHeuristic
from time import time

def random_edge_swap(solution, instance):
    n = len(solution.cycles[0])
    for ci in range_random_start(0, len(solution.cycles)):
        for i in range_random_start(0, n):
            for j in range_random_start(i + 2, n):
                if i == (j + 1) % n:
                    continue

                cycle = solution.cycles[ci].copy()

                _vi_prev, vi, vi_next = neighbor_vertices(cycle, i)
                _vj_prev, vj, vj_next = neighbor_vertices(cycle, j)

                c = cycle[i + 1 : j + 1]
                c.reverse()
                cycle[i + 1 : j + 1] = c

                length = (
                    solution.lengths[ci]
                    - instance[vi][vi_next]
                    - instance[vj][vj_next]
                    + instance[vi][vj]
                    + instance[vi_next][vj_next]
                )

                if ci == 0:
                    return Solution((cycle, solution.cycles[1]),lengths=(length, solution.lengths[1]))
                else:
                    return Solution((solution.cycles[0], cycle),lengths=(solution.lengths[0], length))

def random_vertex_swap(solution, instance):
    n = len(solution.cycles[0])
    for ci in range_random_start(0, len(solution.cycles)):
        for i in range_random_start(0, n):
            for j in range_random_start(i + 1, n):
                cycle = solution.cycles[ci].copy()

                vi_prev, vi, vi_next = neighbor_vertices(cycle, i)
                vj_prev, vj, vj_next = neighbor_vertices(cycle, j)
                if j == i + 1:
                    length = (
                        solution.lengths[ci]
                        - instance[vi_prev][vi]
                        - instance[vj][vj_next]
                        + instance[vi_prev][vj]
                        + instance[vi][vj_next]
                    )
                elif i == (j + 1) % n:
                    length = (
                        solution.lengths[ci]
                        - instance[vj_prev][vj]
                        - instance[vi][vi_next]
                        + instance[vj_prev][vi]
                        + instance[vj][vi_next]
                    )
                else:
                    length = (
                        solution.lengths[ci]
                        + compute_delta(vi_prev, vi, vi_next, vj, instance)
                        + compute_delta(vj_prev, vj, vj_next, vi, instance)
                    )
                cycle[i], cycle[j] = cycle[j], cycle[i]

                if ci == 0:
                    return Solution((cycle, solution.cycles[1]),lengths=(length, solution.lengths[1]))
                else:
                    return Solution((solution.cycles[0], cycle),lengths=(solution.lengths[0], length))

def perturbate(cycles, instance):
    how_many_times = random.randint(1,3)
    solution = Solution(cycles,instance)
    for i in range(how_many_times):
        solution = random_edge_swap(solution,instance)

    how_many_times = random.randint(1, 3)
    solution = Solution(cycles, instance)
    for i in range(how_many_times):
        solution = random_vertex_swap(solution, instance)
    
    return Solution(cycles,instance)


class ILS1(Algorithm):
    def __init__(self, starting_solution, time_limit):
        self.starting_solution = starting_solution
        self.time_limit = time_limit

    def run(self, instance: List[List[int]], start_num: int) -> Solution:
        cycles = self.starting_solution.run(instance, start_num).cycles
        x = Solution(cycles,instance)

        start_time = time()

        while (time() - start_time < self.time_limit):
            x = perturbate(x.cycles, instance)
            y = LocalSearch(False, RandomizedCycleHeuristic(), edge_swap_neighborhood).run(instance)
            if y.total_length < x.total_length:
                x = y
        return x


