from time import time
from typing import List, Callable, Iterator
from algorithm import Algorithm
from solution import Solution


class RandomWalk(Algorithm):
    starting_solution: Algorithm
    neighborhood: Callable[[Solution, List[List[int]]], Iterator[Solution]]

    def __init__(
        self,
        starting_solution: Algorithm,
        neighborhood: Callable[[Solution, List[List[int]]], Iterator[Solution]],
    ):
        self.starting_solution = starting_solution
        self.neighborhood = neighborhood

    def run(self, instance: List[List[int]], start_num: int) -> Solution:
        time_limit = 0.14
        start_time = time()

        best = self.starting_solution().run(instance, start_num)
        current = best
        while time() - start_time < time_limit:
            current = next(self.neighborhood(current, instance))
            if current.total_length < best.total_length:
                best = current

        return best
