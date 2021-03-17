from abc import ABC, abstractmethod
from typing import List
from solution import Solution

class Algorithm(ABC):
    @abstractmethod
    def run(self, instance: List[List[int]]) -> Solution:
        pass
