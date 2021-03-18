from lab1.dummy_algorithm import DummyAlgorithm
from lab1.cycle_heuristic import CycleHeuristic
from read_data import read_data

data = read_data('data/kroA100.tsp')
result = CycleHeuristic().run(data)
print(result)
