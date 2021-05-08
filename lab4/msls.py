from algorithm import Algorithm
from solution import Solution
from typing import List, Tuple, Set
import random
from lab4.local_search import LocalSearch
from lab4.neighborhood import edge_swap_neighborhood
from lab4.randomized_cycle_heuristic import RandomizedCycleHeuristic


class MultipleStartLocalSearch(Algorithm):
    def __init__(self, starting_solution):
        self.starting_solution = starting_solution

    def run(self, instance: List[List[int]], start_num: int) -> Solution:
        cycles = self.starting_solution.run(instance, start_num).cycles
        best = Solution(cycles,instance)
        tmp = list(range(0,200,1))
        if start_num in tmp:
            tmp.remove(start_num)

        start_nums = random.sample(tmp, 99)
        for sn in start_nums:
            c = LocalSearch(False, RandomizedCycleHeuristic(), edge_swap_neighborhood).run(instance, sn)
            x = c
            if x.total_length < best.total_length:
                best = x

        return best
