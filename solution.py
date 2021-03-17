from typing import List, Tuple

class Solution:
    cycles: Tuple[List[int], List[int]]
    lengths: Tuple[int, int]
    total_length: int

    def __init__(self, cycles: Tuple[List[int], List[int]], instance: List[List[int]]):
        self.cycles = cycles
        self.lengths = [0, 0]
        self.total_length = self.score()

    def score(self) -> int:
        return 0

    def is_valid(self) -> bool:
        return True
    
    def __str__(self):
        return f'Solution(cycles={self.cycles}, lengths={self.lengths}, total_length={self.total_length})'
