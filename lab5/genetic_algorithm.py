from time import time
from typing import List, Set, Tuple, NamedTuple
from algorithm import Algorithm
from solution import Solution
from lab2.neighborhood import edge_swap_neighborhood
import random


class GeneticAlgorithm(Algorithm):
    starting_solution: Algorithm
    time_limit: float
    use_local_search: bool
    population: List[Solution]
    population_size: int

    def __init__(
        self,
        time_limit: float,  # in seconds
        starting_solution: Algorithm,
        no_local_search: bool = False,
        population_size: int = 20,
    ):
        self.starting_solution = starting_solution
        self.time_limit = time_limit
        self.use_local_search = not no_local_search
        self.population = []#set()
        self.population_size = population_size

    def run(self, instance: List[List[int]], start_num: int = None) -> Solution:
        start_time = time()

        # Initialize population
        for _i in range(self.population_size):
            #ADD
            self.population.append(self.starting_solution.run(instance, _i))


        while time() - start_time < self.time_limit:
            self.population = sorted(self.population, key=lambda e: e.total_length)
            parent_A = random.randint(0, 19)
            parent_B = random.randint(0, 19)
            while parent_A == parent_B:
                parent_B = random.randint(0, 19)
            solution = self.crossover(self.population[parent_A], self.population[parent_B], instance)

            if solution.total_length < self.population[-1].total_length and self.different(solution): #I WYSTARCZAJĄCO RÓŻNE
                self.population[-1] = solution
                # print(f"{time() - start_time:.3f} Improvement", best.total_length)

        self.population = sorted(self.population, key=lambda e: e.total_length)

        return self.population[0]

    def different(self, solution):
        for e in self.population:
            if e.total_length == solution.total_length:
                return False
            else:
                continue
        return True

    def crossover(
        self, parent1: Solution, parent2: Solution, distances: List[List[int]]
    ) -> Solution:
        child, vertices = remove_vertices(parent1, parent2)
        child.cycles = repair(child.cycles, vertices, distances)
        solution = Solution(child.cycles, distances)
        if self.use_local_search:
            solution =  self.local_search(solution, distances)
        return solution

    def local_search(self, solution: Solution, distances: List[List[int]]) -> Solution:
        improved = True
        best = solution
        while improved:
            improved = False
            for neighbor in edge_swap_neighborhood(best, distances):
                if neighbor.total_length < best.total_length:
                    best = neighbor
                    improved = True
        return best


def get_neighbors(cycle: List[int], i) -> Tuple[int, int]:
    return cycle[(i - 1) % len(cycle)], cycle[(i + 1) % len(cycle)]


# Creates new solution
def remove_vertices(parent1: Solution, parent2: Solution) -> Tuple[Solution, Set[int]]:
    n_vertices = len(parent2.cycles[0]) + len(parent2.cycles[1])

    # Pairs of (predecessor, successor)
    neihgbors = [(-1, -1) for _i in range(n_vertices)]
    for cycle in parent2.cycles:
        for i, vertex in enumerate(cycle):
            neihgbors[vertex] = get_neighbors(cycle, i)

    removed_vertices = set()
    new_cycles = ([], [])
    for cycle_i, cycle in enumerate(parent1.cycles):
        for i, vertex in enumerate(cycle):
            p2_pred, p2_succ = neihgbors[vertex]
            pred, succ = get_neighbors(cycle, i)
            # Check also reverse direction
            if (
                pred != p2_pred
                and succ != p2_succ
                and pred != p2_succ
                and succ != p2_pred
            ):
                # remove vertex
                removed_vertices.add(vertex)
            else:
                # keep vertex
                new_cycles[cycle_i].append(vertex)

    return Solution(new_cycles, lengths=[-1, -1]), removed_vertices


class Candidate(NamedTuple):
    value: int
    vertex: int
    cycle: int
    insert_position: int


def repair(
    cycles: Tuple[List[int], List[int]], vertices: Set[int], distances: List[List[int]]
) -> Tuple[List[int], List[int]]:
    while len(vertices) > 0:
        best_regret = Candidate(-1e9, -1, -1, -1)

        for v in vertices:
            candidate1 = Candidate(1e9, -1, -1, -1)
            candidate2 = Candidate(1e9, -1, -1, -1)

            for cycle_ind, cycle in enumerate(cycles):
                cycle_len = len(cycle)
                if cycle_len > len(cycles[1 - cycle_ind]):
                    continue

                for j in range(cycle_len):
                    v1 = cycle[j]
                    v2 = cycle[(j + 1) % cycle_len]
                    length_diff = (
                        distances[v1][v] + distances[v][v2] - distances[v1][v2]
                    )

                    if length_diff < candidate2.value:
                        candidate2 = Candidate(length_diff, v, cycle_ind, j)
                        if candidate2.value < candidate1.value:
                            candidate1, candidate2 = candidate2, candidate1

            regret = candidate2.value - candidate1.value
            value = 1.8 * regret - candidate1.value
            if value > best_regret.value:
                best_regret = Candidate(
                    value,
                    candidate1.vertex,
                    candidate1.cycle,
                    candidate1.insert_position,
                )

        vertices.remove(best_regret.vertex)
        cycles[best_regret.cycle].insert(
            best_regret.insert_position + 1, best_regret.vertex
        )

    return cycles
