from model.SA import *
from model.Problem import Problem
import time

def test(instance: str):
    time0 = time.time()
    with open(instance) as file:
        p = Problem.from_textIO(file)
    #s = p.empty_solution()
    #s = p.random_solution()
    #p.construction_neighbourhood("allFeasible")

    s = alg.greedy_construction(p)
    #s = alg.beam_search(p, bw=10)
    
    print(f"Is feasible: {s.is_feasible()}")
    print(s)
    print(f"Execution time: {time.time()-time0}")
    
    neighbourhood = p.local_neighbourhood()
    avg_delta = estimate_delta(neighbourhood, s, 100)
    t0 = -avg_delta / math.log(0.5)
    scheduler = geometric(1, 0.99995)
    #scheduler = cosine(t0=t0,t_min=0.01,total=1000_000)

    best = None
    for _ in range(1):
        s = alg.greedy_construction(p)
        candidate, history = sa(problem=p, solution=s, budget=60, p_accept=0.5, scheduler=scheduler, record=True)
        if best is None or candidate.lb < best.lb:
            best = candidate
    #best, history = sa(problem=p, solution=s, budget=60, p_accept=0.5, scheduler=scheduler, record=True)
    #s = alg.first_improvement(p,s)
    #s = alg.best_improvement(p, s)
    #s = alg.sa(p, s, budget=5.0, init_temp=50.0)
    print(f"Is feasible: {s.is_feasible()}")
    print(best)
    print(f"Execution time: {time.time()-time0}")
    return best, history


if __name__ == "__main__":
    import roar_net_api.algorithms as alg
    
    instance = (
        #"tfp_13n_3q_4l_5u_3a_5d.txt"
        #"tfp_131n_27q_4l_5u_10a_10d.txt"
        #"tfp_200n_40q_5l_5u_10a_15d.txt"
        "tfp_300n_60q_5l_5u_10a_40d.txt"
        )
    s,h = test(instance)

    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd

    
    df = pd.DataFrame(h)

    fig, axes = plt.subplots(2, 1, figsize=(12, 6))
    df_sampled = df[df["k"] < 100_000]
    sns.lineplot(data=df_sampled, x="k", y="temp", ax=axes[0])
    sns.lineplot(data=df_sampled, x="k", y="cost", ax=axes[1])
    plt.tight_layout()
    plt.savefig("sa_trace.png")

    
    with open("solution.sol", "w") as out:
        out.write(" ".join(str(t) for t in s.assignments) + "\n")