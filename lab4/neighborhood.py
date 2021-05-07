from itertools import chain
import random
from typing import List, Generator, Iterator
from solution import Solution


def neighbor_vertices(cycle: List[int], i: int):
    n = len(cycle)
    return cycle[(i - 1) % n], cycle[i], cycle[(i + 1) % n]


def range_random_start(start: int, stop: int) -> Iterator[int]:
    if start >= stop:
        return range(start, stop)
    r = random.randrange(start, stop)
    return chain(range(r, stop), range(start, r))


def compute_delta(
    pred: int,
    middle: int,
    succ: int,
    replacement: int,
    distances: List[List[int]],
):
    return (
        distances[pred][replacement]
        + distances[replacement][succ]
        - distances[pred][middle]
        - distances[middle][succ]
    )


def between_cycle_swap(
    solution: Solution, distances: List[List[int]]
) -> Generator[Solution, None, None]:
    n = len(solution.cycles[0])

    for i in range_random_start(0, n):
        for j in range_random_start(0, n):
            cycles = solution.cycles[0].copy(), solution.cycles[1].copy()
            vi_prev, vi, vi_next = neighbor_vertices(cycles[0], i)
            vj_prev, vj, vj_next = neighbor_vertices(cycles[1], j)
            length0 = solution.lengths[0] + compute_delta(
                vi_prev, vi, vi_next, vj, distances
            )
            length1 = solution.lengths[1] + compute_delta(
                vj_prev, vj, vj_next, vi, distances
            )

            cycles[0][i], cycles[1][j] = cycles[1][j], cycles[0][i]

            yield Solution(cycles, lengths=(length0, length1))


def vertex_swap(
    solution: Solution, distances: List[List[int]]
) -> Generator[Solution, None, None]:
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
                        - distances[vi_prev][vi]
                        - distances[vj][vj_next]
                        + distances[vi_prev][vj]
                        + distances[vi][vj_next]
                    )
                elif i == (j + 1) % n:
                    length = (
                        solution.lengths[ci]
                        - distances[vj_prev][vj]
                        - distances[vi][vi_next]
                        + distances[vj_prev][vi]
                        + distances[vj][vi_next]
                    )
                else:
                    length = (
                        solution.lengths[ci]
                        + compute_delta(vi_prev, vi, vi_next, vj, distances)
                        + compute_delta(vj_prev, vj, vj_next, vi, distances)
                    )
                cycle[i], cycle[j] = cycle[j], cycle[i]

                if ci == 0:
                    yield Solution(
                        (cycle, solution.cycles[1]),
                        lengths=(length, solution.lengths[1]),
                    )
                else:
                    yield Solution(
                        (solution.cycles[0], cycle),
                        lengths=(solution.lengths[0], length),
                    )


def edge_swap(
    solution: Solution, distances: List[List[int]]
) -> Generator[Solution, None, None]:
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
                    - distances[vi][vi_next]
                    - distances[vj][vj_next]
                    + distances[vi][vj]
                    + distances[vi_next][vj_next]
                )

                if ci == 0:
                    yield Solution(
                        (cycle, solution.cycles[1]),
                        lengths=(length, solution.lengths[1]),
                    )
                else:
                    yield Solution(
                        (solution.cycles[0], cycle),
                        lengths=(solution.lengths[0], length),
                    )


def vertex_swap_neighborhood(solution: Solution, distances: List[List[int]]):
    x = random.randint(0, 1)
    if x == 0:
        return chain(
            between_cycle_swap(solution, distances), vertex_swap(solution, distances)
        )
    return chain(
        vertex_swap(solution, distances), between_cycle_swap(solution, distances)
    )


def edge_swap_neighborhood(solution: Solution, distances: List[List[int]]):
    x = random.randint(0, 1)
    if x == 0:
        return chain(
            between_cycle_swap(solution, distances), edge_swap(solution, distances)
        )
    return chain(
        edge_swap(solution, distances), between_cycle_swap(solution, distances)
    )
