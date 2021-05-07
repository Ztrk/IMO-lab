from typing import Iterator, Callable, List
from algorithm import Algorithm
from solution import Solution


class LocalSearch(Algorithm):
    is_greedy: bool
    starting_solution: Algorithm
    neighborhood: Callable[[Solution, List[List[int]]], Iterator[Solution]]

    def __init__(
        self,
        is_greedy: bool,
        starting_solution: Algorithm,
        neighborhood: Callable[[Solution, List[List[int]]], Iterator[Solution]],
    ):
        self.is_greedy = is_greedy
        self.starting_solution = starting_solution
        self.neighborhood = neighborhood

    def run(self, instance: List[List[int]], start_num: int = None) -> Solution:
        best = self.starting_solution.run(instance, start_num)
        improved = True
        while improved:
            improved = False
            for neighbor in self.neighborhood(best, instance):
                if best.total_length > neighbor.total_length:
                    best = neighbor
                    improved = True
                    if self.is_greedy:
                        break

        return best
