import random
from typing import List, Set, Tuple, NamedTuple
from solution import Solution


class Candidate(NamedTuple):
    value: int
    vertex: int
    cycle: int
    insert_position: int


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


def destroy_repair(
    solution: Solution, distances: List[List[int]], destroy_fraction: float
) -> Solution:
    destroy_start0 = random.randint(0, len(solution.cycles[0]) - 1)
    destroy_start1 = random.randint(0, len(solution.cycles[0]) - 1)

    new_cycles = solution.cycles[0].copy(), solution.cycles[1].copy()
    _, removed_vertices0 = destroy(destroy_start0, new_cycles[0], destroy_fraction)
    _, removed_vertices1 = destroy(destroy_start1, new_cycles[1], destroy_fraction)

    new_cycles = repair(new_cycles, removed_vertices0 | removed_vertices1, distances)

    return Solution(new_cycles, distances)
