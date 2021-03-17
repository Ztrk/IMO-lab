from algorithm import Algorithm
from typing import List
from solution import Solution

class DummyAlgorithm(Algorithm):
    def run(self, instance: List[List[int]]) -> Solution:
        n = len(instance)
        half = int((n - 1)/2)
        cycle1 = [i for i in range(half + 1)]
        cycle2 = [i for i in range(half + 1, n)]

        return Solution((cycle1, cycle2), instance)
