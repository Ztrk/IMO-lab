import random
from time import time
from typing import List, Set, Tuple, NamedTuple
from algorithm import Algorithm
from solution import Solution
from lab2.neighborhood import edge_swap_neighborhood


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
        self.population = []
        self.population_size = population_size

    def run(self, instance: List[List[int]], start_num: int = None) -> Solution:
        start_time = time()

        # Initialize population
        for _i in range(self.population_size):
            # ADD
            self.population.append(self.starting_solution.run(instance, _i))

        while time() - start_time < self.time_limit:
            self.population.sort(key=lambda e: e.total_length)
            parent_a = random.randrange(0, self.population_size)
            parent_b = random.randrange(0, self.population_size)
            while parent_a == parent_b:
                parent_b = random.randrange(0, self.population_size)

            solution = self.crossover(
                self.population[parent_a], self.population[parent_b], instance
            )

            if solution.total_length < self.population[-1].total_length and self.different(solution):
                self.population[-1] = solution
                # print(f"{time() - start_time:.3f} Improvement, Score: ", solution.total_length)

        self.population.sort(key=lambda e: e.total_length)

        return self.population[0]

    def different(self, solution):
        for e in self.population:
            if e.total_length == solution.total_length:
                return False
        return True

    def crossover(
        self, parent1: Solution, parent2: Solution, distances: List[List[int]]
    ) -> Solution:
        child, vertices = remove_vertices(parent1, parent2)

        if random.uniform(0, 1) < 0.2:
            destroy_start0 = random.randrange(0, len(child.cycles[0]))
            destroy_start1 = random.randrange(0, len(child.cycles[1]))
            _, removed_vertices0 = destroy(destroy_start0, child.cycles[0], 0.2)
            _, removed_vertices1 = destroy(destroy_start1, child.cycles[1], 0.2)
            vertices |= removed_vertices0 | removed_vertices1

        child.cycles = repair(child.cycles, vertices, distances)
        solution = Solution(child.cycles, distances)

        if self.use_local_search:
            solution = self.local_search(solution, distances)
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


def destroy(
    start: int, cycle: List[int], destroy_fraction: float
) -> Tuple[List[int], Set[int]]:
    """
    Removes part of the cycle in place
    Returns cycle and set of removed vertices
    """
    n = len(cycle)
    to_destroy = int(destroy_fraction * n)

    removed_vertices = set(cycle[start : start + to_destroy])
    cycle[start : start + to_destroy] = []

    if start + to_destroy > n:
        removed_vertices.update(cycle[0 : start + to_destroy - n])
        cycle[0 : start + to_destroy - n] = []

    return cycle, removed_vertices

def remove_vertices_cycle(cycle1: List[int], cycle2: List[int]) -> Tuple[List[int], Set[int]]:
    n_vertices = 2 * len(cycle2)

    # Pairs of (predecessor, successor)
    neihgbors = [(-1, -1) for _i in range(n_vertices)]
    for i, vertex in enumerate(cycle2):
        neihgbors[vertex] = get_neighbors(cycle2, i)

    removed_vertices = set()
    new_cycle = []
    for i, vertex in enumerate(cycle1):
        p2_pred, p2_succ = neihgbors[vertex]
        pred, succ = get_neighbors(cycle1, i)
        # Check if vertex has no common edges with cycle2, check also reverse direction
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
            new_cycle.append(vertex)

    return new_cycle, removed_vertices

# Creates new solution
def remove_vertices(parent1: Solution, parent2: Solution) -> Tuple[Solution, Set[int]]:
    cycle_a1, removed_vertices_a1 = remove_vertices_cycle(parent1.cycles[0], parent2.cycles[0])
    cycle_a2, removed_vertices_a2 = remove_vertices_cycle(parent2.cycles[1], parent1.cycles[1])
    removed_vertices_a2 = set(parent1.cycles[1]) - set(cycle_a2)

    cycle_b1, removed_vertices_b1 = remove_vertices_cycle(parent1.cycles[0], parent2.cycles[1])
    cycle_b2, removed_vertices_b2 = remove_vertices_cycle(parent2.cycles[0], parent1.cycles[1])
    removed_vertices_b2 = set(parent1.cycles[1]) - set(cycle_b2)

    if len(cycle_a1) + len(cycle_a2) >= len(cycle_b1) + len(cycle_b2):
        return (
            Solution((cycle_a1, cycle_a2), lengths=[-1, -1]),
            removed_vertices_a1 | removed_vertices_a2
        )
    else:
        return (
            Solution((cycle_b1, cycle_b2), lengths=[-1, -1]),
            removed_vertices_b1 | removed_vertices_b2
        )


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
