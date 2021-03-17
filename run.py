from lab1.dummy_algorithm import DummyAlgorithm
from read_data import read_data

data = read_data('data/kroA100.tsp')
result = DummyAlgorithm().run(data)
print(result)
