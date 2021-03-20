from typing import List, Tuple, Set
from algorithm import Algorithm
from solution import Solution


class NearestNeighbor(Algorithm):
    def run(self, instance: List[List[int]], start_num: int) -> Solution:
        n = len(instance)
        max_len = (n + 1) // 2
        cycles: Tuple[List[int], List[int]] = self.starting_solution(instance, start_num)
        vertices: Set[int] = set(range(n))
        vertices.remove(cycles[0][0])
        vertices.remove(cycles[1][0])
        total_length = 0
        prev_added = [cycles[0][0],cycles[1][0]]

        for i in range(n - 2):
            best_length = 1e9
            best_vertice = -1
            best_cycle = -1
            best_insert_position = -1

            for cycle_ind, cycle in enumerate(cycles):
                cycle_len = len(cycle)
                if cycle_len >= max_len:
                    continue

                candidates = dict(zip(range(0,n),instance[prev_added[cycle_ind]]))
                sorted_candidates = sorted(instance[prev_added[cycle_ind]])
                v = -1
                for sc in sorted_candidates:
                    best_candidates = [k for k, v in candidates.items() if v == sc]
                    for bc in best_candidates:
                        if bc in vertices:
                            v = bc
                            break
                    if v != -1:
                        break

                for j in range(cycle_len):
                    v1 = cycle[j]
                    v2 = cycle[(j + 1) % cycle_len]
                    length_diff = instance[v1][v] + instance[v][v2] - instance[v1][v2]
                    if length_diff < best_length:
                        best_length = length_diff
                        best_vertice = v
                        best_cycle = cycle_ind
                        best_insert_position = j

            total_length += best_length
            vertices.remove(best_vertice)
            prev_added[best_cycle] = best_vertice
            cycles[best_cycle].insert(best_insert_position + 1, best_vertice)

        return Solution(cycles, instance)

    def starting_solution(self, instance: List[List[int]], start_num: int) -> Tuple[List[int], List[int]]:
        return [start_num], [int(instance[start_num].index(max(instance[start_num])))]
