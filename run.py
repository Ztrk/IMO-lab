from typing import List
from time import time
from lab1.cycle_heuristic import CycleHeuristic
from lab1.nearest_neighbor import NearestNeighbor
from lab1.cycle_heuristic_regret import CycleHeuristicRegret
from lab2.local_search import LocalSearch
from lab2.neighborhood import vertex_swap_neighborhood, edge_swap_neighborhood
from lab2.random_algorithm import RandomAlgorithm
from lab2.random_walk import RandomWalk
from lab3.local_search_LM import LocalSearchLM
from lab3.local_search_CM import LocalSearchCM
from lab4.ils2 import ILS2
from lab4.ils1 import ILS1
from lab4.msls import MultipleStartLocalSearch
from lab4.randomized_cycle_heuristic import RandomizedCycleHeuristic
from lab5.genetic_algorithm import GeneticAlgorithm
from lab6.genetic_algorithm import GeneticAlgorithm as ImprovedGeneticAlgorithm
from algorithm import Algorithm
from solution import Solution
from read_data import read_data, read_data_visualization
from vizualization import visualize


def experiment(algorithms: List[Algorithm], algorithm_names: List[str]):
    for file in ["data/kroB200.tsp"]: #"data/kroA200.tsp",
        data = read_data(file)
        data_vis = read_data_visualization(file)
        print("Instancja: {}".format(file))

        for index, algorithm in enumerate(algorithms):
            results = []
            times = []

            best_result = Solution(([], []), lengths=([1e9, 1e9]))
            for i in range(0, 10):  # 100
                start_time = time()
                result = algorithm.run(data, i)
                if best_result.total_length > result.total_length:
                    best_result = result
                results.append(result.total_length)
                times.append((time() - start_time) * 1000)

            print("Dla algorytmu: {}".format(algorithm_names[index]))
            print("średnia suma długości cykli: {}".format(sum(results) / len(results)))
            print("minimalna suma długości cykli: {}".format(min(results)))
            print("maksymalna suma długości cykli: {}".format(max(results)))

            print("średni czas wykonania: {:0f} ms".format(sum(times) / len(times)))
            print("minimalny czas wykonania: {:0f} ms".format(min(times)))
            print("maksymalny czas wykonania: {:0f} ms".format(max(times)))

            print()
            visualize(
                best_result.cycles,
                data_vis,
                best_result.lengths,
                best_result.total_length,
                algorithm_names[index],
                file,
            )


def lab1():
    experiment(
        [NearestNeighbor(), CycleHeuristic(), CycleHeuristicRegret()],
        ["Nearest neighbor", "Greedy cycle", "Regret heuristic"],
    )


def lab2():
    algorithms = []
    for is_greedy in [True, False]:
        for neighborhood in [vertex_swap_neighborhood, edge_swap_neighborhood]:
            for starting_solution in [CycleHeuristicRegret(), RandomAlgorithm()]:
                algorithms.append(
                    LocalSearch(is_greedy, starting_solution, neighborhood)
                )
    algorithms.append(RandomWalk(RandomAlgorithm(), edge_swap_neighborhood))

    algorithm_names = []
    for version in ["zachłanne", "strome"]:
        for neighborhood in ["zamiana wierzchołków", "zamiana krawędzi"]:
            for starting_solution in [
                "rozwiązanie początkowe zachłanne",
                "rozwiązanie początkowe losowe",
            ]:
                algorithm_names.append(
                    f"Przeszukiwanie lokalne - {version}, {neighborhood}, {starting_solution}"
                )
    algorithm_names.append("Losowe błądzenie")
    experiment(algorithms, algorithm_names)


def lab2_random_walk():
    experiment(
        [RandomWalk(RandomAlgorithm(), edge_swap_neighborhood)], ["Losowe błądzenie"]
    )


def lab3():
    experiment(
        [  # CycleHeuristicRegret(),
            # LocalSearch(False, RandomAlgorithm(), edge_swap_neighborhood),
            LocalSearchCM(RandomAlgorithm()),
            LocalSearchLM(RandomAlgorithm()),
        ],
        [  # "Regret heuristic",
            # "Przeszukiwanie lokalne - strome, zamiana krawędzi, rozwiązanie początkowe losowe",
            "Przeszukiwanie lokalne - ruchy kandydackie",
            "Przeszukiwanie lokalne - wykorzystanie ocen ruchów z poprzednich iteracji",
        ],
    )


def lab4():
    """
    experiment(
        [
            ILS2(
                time_limit=310,
                destroy_fraction=0.2,
                no_local_search=False,
                starting_solution=RandomizedCycleHeuristic(),
            ),
            ILS2(
                time_limit=310,
                destroy_fraction=0.2,
                no_local_search=True,
                starting_solution=RandomizedCycleHeuristic(),
            )
        ],
        ["ILS2", "ILS2A"],
    )
    """
    experiment(
        #[MultipleStartLocalSearch(LocalSearch(False, RandomizedCycleHeuristic(), edge_swap_neighborhood))], ["Multiple start local search"]
        [ILS1(LocalSearch(False, RandomizedCycleHeuristic(), edge_swap_neighborhood), 310)], ["ILS1"]
    )


def lab5():
    experiment(
        [GeneticAlgorithm(310, LocalSearch(False, RandomizedCycleHeuristic(), edge_swap_neighborhood), False),
            GeneticAlgorithm(310, LocalSearch(False, RandomizedCycleHeuristic(), edge_swap_neighborhood), True)
        ],
        [
            "HAE z LP",
            "HAE bez LP",
        ],
    )

def lab6():
    experiment(
        [
            ImprovedGeneticAlgorithm(
                310,
                LocalSearch(False, RandomizedCycleHeuristic(), edge_swap_neighborhood),
                no_local_search=False
            ),
            ImprovedGeneticAlgorithm(
                310,
                LocalSearch(False, RandomizedCycleHeuristic(), edge_swap_neighborhood),
                no_local_search=True
            )
        ],
        [
            "HAE z LP",
            "HAE bez LP",
        ],
    )


lab6()
