from typing import List, Tuple
import itertools

class Solution:
    cycles: Tuple[List[int], List[int]]
    lengths: Tuple[int, int]
    total_length: int

    def __init__(self, cycles: Tuple[List[int], List[int]], instance: List[List[int]]):
        self.cycles = cycles
        self.lengths = [0, 0]
        self.total_length = 0
        self.check_validity(instance)
        self.score(instance)

    def score(self, instance: List[List[int]]) -> int:
        for i, cycle in enumerate(self.cycles):
            n = len(cycle)
            length = 0
            for v1, v2 in zip(cycle[:n - 1], cycle[1:]):
                length += instance[v1][v2]
            length += instance[cycle[0]][cycle[n - 1]]
            self.lengths[i] = length
        self.total_length = sum(self.lengths)

    def check_validity(self, instance: List[List[int]]) -> bool:
        n = len(instance)
        cycles = self.cycles
        len1 = len(cycles[0])
        len2 = len(cycles[1])

        if abs(len1 - len2) > 1:
            raise ValueError('Both paths must contain half or half - 1 of vertices')
        if len1 + len2 != n:
            raise ValueError('Paths must contain every vertex exactly once')
        
        is_present = [False for i in range(n)]
        for v in itertools.chain(cycles[0], cycles[1]):
            if v >= n or v < 0:
                raise ValueError('Vertex index must be between 0 and n - 1')
            if is_present[v]:
                raise ValueError('Paths must contain every vertex exactly once')
            is_present[v] = True
        return True

    def __str__(self):
        return f'Solution(cycles={self.cycles}, lengths={self.lengths}, total_length={self.total_length})'
