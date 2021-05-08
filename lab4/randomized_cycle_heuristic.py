from typing import List, Tuple, Set, NamedTuple, Iterable
import itertools
import random
from algorithm import Algorithm
from solution import Solution
import random


class Candidate(NamedTuple):
    length_diff: int
    vertex: int
    cycle: int
    insert_position: int


class RandomizedCycleHeuristic(Algorithm):
    def run(self, instance: List[List[int]], starting_vertex: int = None) -> Solution:
        n = len(instance)
        max_len = (n + 1) // 2
        cycles: Tuple[List[int], List[int]] = self.starting_solution(starting_vertex, n, instance)
        vertices: Set[int] = set(range(n))
        vertices.remove(cycles[0][0])
        vertices.remove(cycles[1][0])

        vertices = list(vertices)
        vertices = random.sample(vertices, len(vertices))
        while len(vertices) > 0:
            candidate1 = Candidate(1e9, -1, -1, -1)
            candidate2 = Candidate(1e9, -1, -1, -1)

            vertices = random.sample(vertices, len(vertices))
            for v in vertices:
                for cycle_ind, cycle in enumerate(cycles):
                    cycle_len = len(cycle)
                    if cycle_len >= max_len:
                        continue

                    for j in range(cycle_len):
                        v1 = cycle[j]
                        v2 = cycle[(j + 1) % cycle_len]
                        length_diff = instance[v1][v] + instance[v][v2] - instance[v1][v2]
                        if length_diff < candidate1.length_diff:
                            candidate1 = Candidate(length_diff, v, cycle_ind, j)
                        if length_diff < candidate2.length_diff:
                            candidate2 = Candidate(length_diff, v, cycle_ind, j)
            dec= random.randint(0, 1)
            if dec == 0:
                candidate = candidate1
            else:
                candidate = candidate2
            vertices.remove(candidate.vertex)
            cycles[candidate.cycle].insert(candidate.insert_position + 1, candidate.vertex)

        return Solution(cycles, instance)

    def starting_solution(self, starting_vertex: int, n: int, instance: List[List[int]]) -> Tuple[List[int], List[int]]:
        v1 = random.randint(0, n - 1)
        v2 = random.randint(0, n - 1)
        while v2 == v1:
            v2 = random.randint(0, n - 1)
        return ([v1], [v2])

