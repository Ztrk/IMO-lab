from lab1.dummy_algorithm import DummyAlgorithm
from lab1.cycle_heuristic import CycleHeuristic
from lab1.nearest_neighbor import NearestNeighbor
from read_data import read_data, read_data_visualization
from vizualization import visualize

for file in ['data/kroA100.tsp', 'data/kroB100.tsp']:
    data = read_data(file)
    data_vis = read_data_visualization(file)
    print("Instancja: {}".format(file))
    algorithm_names = ["Nearest neighbor", "Gready cycle", "Regret heuristics"]
    for index, algorithm in enumerate([NearestNeighbor(), CycleHeuristic()]): #TODO: ADD REGRET ALGO
        results = []
        best_result = algorithm.run(data, 0)
        for i in range(0,100):
            result = algorithm.run(data,i)
            if best_result.total_length > result.total_length:
                best_result = result
            results.append(result.total_length)
        print("Dla algorytmu: {}".format(algorithm_names[index]))
        print("minimalna suma długości cykli: {}".format(min(results)))
        print("maksymalna suma długości cykli: {}".format(max(results)))
        print("średnia suma długości cykli: {}".format(sum(results)/len(results)))
        visualize(best_result.cycles, data_vis, best_result.lengths, best_result.total_length, algorithm_names[index], file)


