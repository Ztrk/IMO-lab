from lab2.local_search import LocalSearch
from lab2.neighborhood import edge_swap_neighborhood
from lab2.random_algorithm import RandomAlgorithm
from read_data import read_data
from solution import Solution
import numpy as np
import matplotlib.pyplot as plt


def similarity_vertex(x, y):
    x_cycles = x.cycles
    y_cycles = y.cycles
    if len(set(x.cycles[0]) & set(y.cycles[0])) > len(set(x.cycles[0]) & set(y.cycles[1])):
        return len(set(x.cycles[0]) & set(y.cycles[0])) + len(set(x.cycles[1]) & set(y.cycles[1]))
    return len(set(x.cycles[0]) & set(y.cycles[1])) + len(set(x.cycles[1]) & set(y.cycles[0]))


def similarity_edges(x, y):
    x_edges = []
    y_edges = []
    for num in [0,1]:
        for i in range(len(x.cycles[num]) - 1):
            x_edges.append((x.cycles[num][i],x.cycles[num][i+1]))
        for i in range(len(y.cycles[num]) - 1):
            y_edges.append((y.cycles[num][i], y.cycles[num][i + 1]))
        x_edges.append((x.cycles[num][-1],x.cycles[num][0]))
        y_edges.append((y.cycles[num][-1], y.cycles[num][0]))

    return len(set(x_edges) & set(y_edges))


def count_corelation(x, y):
    return np.corrcoef(x, y)[0,1]


for file, n in zip(["C:/Users/Kornelia/Desktop/STUDIA/IMO/IMO-lab/data/kroB200.tsp", "C:/Users/Kornelia/Desktop/STUDIA/IMO/IMO-lab/data/kroA200.tsp"],["kroA200","kroB200"]):
    data = read_data(file)
    results = []
    results_len = []
    best_result = Solution(([], []), lengths=([1e9, 1e9]))
    for i in range(0, 1000):
        if i% 100 == 0:
            print(i)
        result = LocalSearch(True, RandomAlgorithm(), edge_swap_neighborhood).run(data, i//5)
        if best_result.total_length > result.total_length:
            best_result = result
        results.append(result)
        results_len.append(result.total_length)
    results.remove(best_result)
    results_len.remove(best_result.total_length)
    dict_res = {k:v for k,v in zip(results,results_len)}
    dict_res = {k: v for k, v in sorted(dict_res.items(), key=lambda item: item[1])}
    results = list(dict_res.keys())
    results_len = list(dict_res.values())
    res_edges = []
    res_edges_best = []
    res_vertex = []
    res_vertex_best = []

    for i in range(0, 999):
        x = results[i]
        sim_edges = []
        sim_vertex = []
        ys = results.copy()
        ys.remove(x)
        for y_ in ys:
            sim_edges.append(similarity_edges(x, y_))
            sim_vertex.append(similarity_vertex(x, y_))
        res_edges.append(np.mean(sim_edges))
        res_vertex.append(np.mean(sim_vertex))
        res_edges_best.append(similarity_edges(x, best_result))
        res_vertex_best.append(similarity_vertex(x, best_result))

    for r, name in zip([res_edges, res_edges_best], ["średnie", "do_najlepszego"]):
        fig, ax = plt.subplots()
        line, = ax.plot(results_len, r, 'o')
        corelation = 'Korelacja: ' + str(round(count_corelation(results_len, r), 2))
        ax.set(xlabel='x, ' + corelation, ylabel='podobieństwo',
           title='Podobieństwo pod kątem krawędzi')

        plt.title("Podobieństwo krawędzi - " + name)
        plt.savefig(str(n) + str(name) +'kraw.png')
        plt.show()


    for r, name in zip([res_vertex, res_vertex_best], ["średnie", "do_najlepszego"]):
        fig, ax = plt.subplots()
        line, = ax.plot(results_len, r, 'o')
        corelation = 'Korelacja: ' + str(round(count_corelation(results_len, r), 2))
        ax.set(xlabel='x, ' + corelation, ylabel='średnie podobieństwo',
            title='Podobieństwo pod kątem wierzchołków')
        plt.title("Podobieństwo wierzchołków - " + name)
        plt.savefig(str(n) + str(name) + 'wierzch.png', bbox_inches='tight')
        plt.show()