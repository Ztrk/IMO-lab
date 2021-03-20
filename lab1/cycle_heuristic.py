from typing import List, Tuple, Set, NamedTuple, Iterable
import itertools
import random
from algorithm import Algorithm
from solution import Solution
from read_data import read_data

class Candidate(NamedTuple):
    length_diff: int
    vertex: int
    cycle: int
    insert_position: int

class CycleHeuristic(Algorithm):
    def run(self, instance: List[List[int]], starting_vertex: int = None) -> Solution:
        n = len(instance)
        max_len = (n + 1)//2
        cycles: Tuple[List[int], List[int]] = self.starting_solution(starting_vertex, n, instance)
        vertices: Set[int] = set(range(n))
        vertices.remove(cycles[0][0])
        vertices.remove(cycles[1][0])

        while len(vertices) > 0:
            candidate = Candidate(1e9, -1, -1, -1)

            for v in vertices:
                for cycle_ind, cycle in enumerate(cycles):
                    cycle_len = len(cycle)
                    if cycle_len >= max_len:
                        continue

                    for j in range(cycle_len):
                        v1 = cycle[j]
                        v2 = cycle[(j + 1) % cycle_len]
                        length_diff = instance[v1][v] + instance[v][v2] - instance[v1][v2]
                        if length_diff < candidate.length_diff:
                            candidate = Candidate(length_diff, v, cycle_ind, j)
            
            vertices.remove(candidate.vertex)
            cycles[candidate.cycle].insert(candidate.insert_position + 1, candidate.vertex)

        return Solution(cycles, instance)

    def starting_solution(self, starting_vertex: int, n: int, instance: List[List[int]]) -> Tuple[List[int], List[int]]:
        v1 = starting_vertex
        if v1 is None:
            v1 = random.randint(0, n - 1)
        v2 = 0
        for v in range(0, n):
            if instance[v1][v] > instance[v1][v2]:
                v2 = v
        # v2 = random.randint(0, n - 1)
        # while v2 == v1:
            # v2 = random.randint(0, n - 1)
        return ([v1], [v2])

    def get_closest(self, v: int, vertices: Iterable[int], distance: List[List[int]]):
        result = -1
        for v1 in vertices:
            if result == -1:
                result = v1
            elif distance[v1][v] < distance[result][v]:
                result = v1
        return result


def run_instance(filepath, runs):
    data1 = read_data(filepath)
    alg = CycleHeuristic()
    solution_lengths = []
    for i in range(runs):
        solution = alg.run(data1, i)
        solution_lengths.append(solution.total_length)
    print('Mean: ', sum(solution_lengths) / runs)
    print('Min: ', min(solution_lengths))
    print('Max: ', max(solution_lengths))

def experiment(runs: int = 100):
    print('kroA100')
    run_instance('data/kroA100.tsp', runs)

    print('\nkroB100')
    run_instance('data/kroB100.tsp', runs)
