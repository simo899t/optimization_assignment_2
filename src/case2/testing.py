import random, time
from collections.abc import Iterable
from typing import Self, TextIO

from roar_net_api.operations import ( # Interface for the ROAR-NET-API
    SupportsCopySolution,
    SupportsObjectiveValue,
    SupportsLowerBound,
    SupportsConstructionNeighbourhood,
    SupportsLocalNeighbourhood,
    SupportsEmptySolution,
    SupportsRandomSolution,
    SupportsApplyMove,
    SupportsLowerBoundIncrement,
    SupportsObjectiveValueIncrement,
    SupportsMoves,
    SupportsRandomMovesWithoutReplacement,
    SupportsRandomMove,

)
from model.Problem import Problem
def test(instance: str):
    t0 = time.time()
    with open(instance) as file:
        p = Problem.from_textIO(file)
    p.empty_solution()

    p.construction_neighbourhood("balanced")
    s = alg.greedy_construction(p)
    print(f"Is feasible: {s.is_feasible()}")
    print(s)
    print(f"Execution time: {time.time()-t0}")
    #s = alg.sa(p, s, budget=5.0, init_temp=50.0)
    #print(s)



if __name__ == "__main__":
    import roar_net_api.algorithms as alg
    
    instance = (
        #"tfp_13n_3q_4l_5u_3a_5d.txt"
        #"tfp_131n_27q_4l_5u_10a_10d.txt"
        #"tfp_200n_40q_5l_5u_10a_15d.txt"
        "tfp_300n_60q_5l_5u_10a_40d.txt"
        )
    test(instance)

    with open(instance) as file:
        p = Problem.from_textIO(file)

    c_heuristic = (
        #"balanced"
        #"constrained"
        #"hybrid"
        "greedy"
        )

    p.construction_neighbourhood(c_heuristic)

    s = p.empty_solution()
    #s = p.random_solution()
    #s = p.worst_solution()

    s = alg.greedy_construction(p)
    #s = alg.beam_search(p,s,10)
    #s = alg.grasp(p, budget=10) #<- wont work :(

    l_heuristic = (
        #"random"
        #"constrained"
        #"hybrid"
        "greedy"
        )
    
    

    p.local_neighbourhood("greedy")

    
    s = alg.best_improvement(p, s)
    #s = alg.first_improvement(p,s)
    #s = alg.sa(p, s, budget=5.0, init_temp=50.0)

    
    with open("solution.sol", "w") as out:
        out.write(" ".join(str(t) for t in s.assignments) + "\n")