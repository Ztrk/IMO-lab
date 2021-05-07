from time import time
from typing import Iterator, Callable, List
from algorithm import Algorithm
from solution import Solution
from lab4.neighborhood import edge_swap_neighborhood
from lab4.destroy_repair import destroy_repair


class ILS2(Algorithm):
    is_greedy: bool
    starting_solution: Algorithm
    neighborhood: Callable[[Solution, List[List[int]]], Iterator[Solution]]
    time_limit: float
    destroy_fraction: float
    use_local_search: bool

    def __init__(
        self,
        time_limit: float,  # in seconds
        destroy_fraction: float,
        starting_solution: Algorithm,
        no_local_search: bool = False,
        is_greedy: bool = False,
        neighborhood: Callable[
            [Solution, List[List[int]]], Iterator[Solution]
        ] = edge_swap_neighborhood,
    ):
        self.is_greedy = is_greedy
        self.starting_solution = starting_solution
        self.neighborhood = neighborhood
        self.time_limit = time_limit
        self.destroy_fraction = destroy_fraction
        self.use_local_search = not no_local_search

    def run(self, instance: List[List[int]], start_num: int = None) -> Solution:
        start_time = time()
        best = self.starting_solution.run(instance, start_num)
        if self.use_local_search:
            best = self.local_search(best, instance)
        # print(f"{time() - start_time:.3f} Starting solution", best.total_length)

        while time() - start_time < self.time_limit:
            solution = destroy_repair(best, instance, self.destroy_fraction)
            if self.use_local_search:
                solution = self.local_search(solution, instance)

            if solution.total_length < best.total_length:
                best = solution
                # print(f"{time() - start_time:.3f} Improvement", best.total_length)

        return best

    def local_search(self, solution: Solution, distances: List[List[int]]) -> Solution:
        improved = True
        best = solution
        while improved:
            improved = False
            for neighbor in self.neighborhood(best, distances):
                if neighbor.total_length < best.total_length:
                    best = neighbor
                    improved = True
                    if self.is_greedy:
                        break
        return best
