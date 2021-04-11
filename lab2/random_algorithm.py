import random
from typing import List
from algorithm import Algorithm
from solution import Solution


class RandomAlgorithm(Algorithm):
    def run(self, instance: List[List[int]], start_num: int = None) -> Solution:
        n = len(instance)
        vertices = list(range(n))
        vertices.remove(start_num)

        cycle1 = [start_num]
        cycle2 = []

        while len(vertices) > 0:
            cycle = cycle2 if len(cycle1) > len(cycle2) else cycle1
            index = random.randrange(0, len(vertices))
            vertice = vertices.pop(index)

            cycle.append(vertice)

        return Solution((cycle1, cycle2), instance)
