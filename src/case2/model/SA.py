import math
import random
import time
from collections.abc import Callable
from .Solution import Solution


def estimate_delta(neighbourhood, solution: Solution, n_samples: int = 100) -> float:
    """
    Returns the average objective_value_increment over n_samples of random moves
    """
    deltas = []
    for _ in range(n_samples):
        move = neighbourhood.random_move(solution)
        if move is None:
            break
        incr = move.objective_value_increment(solution)
        if incr > 0:
            deltas.append(incr)
    return sum(deltas) / len(deltas) if deltas else 1.0


def geometric(t0: float, cooling: float = 0.999) -> Callable[[int], float]:
    """
    Geometric decay for the SA method
    """
    def schedule(k: int) -> float:
        return t0 * (cooling ** k)
    return schedule


def cosine(t0: float, t_min: float = 1.0, total: int = 1_000_000) -> Callable[[int], float]:
    """
    Cosine decay for the SA method
    """
    def schedule(k: int) -> float:
        progress = min(k / total, 1.0)
        return t_min + (t0 - t_min) / 2 * (1 + math.cos(math.pi * progress))
    return schedule


def sa(
    problem,
    solution: Solution,
    budget: float = 60.0,
    p_accept: float = 0.5,
    scheduler: Callable[[int], float] = None,
    record: bool = False,
) -> tuple[Solution, list] | Solution:
    """
    Simulated Annealing (SA), using a scheduler, for the assignment problem implemented using `ROAR-NET-API`
    """

    neighbourhood = problem.local_neighbourhood()
    s = solution.copy_solution()
    best = s.copy_solution()

    delta = estimate_delta(neighbourhood, s)
    t0 = -delta / math.log(p_accept)
    if scheduler is None:
        scheduler = geometric(t0)

    history = []
    t_start = time.time()
    k = 0
    while time.time() - t_start < budget:
        move = neighbourhood.random_move(s)
        if move is None:
            break
        incr = move.objective_value_increment(s)
        temp = scheduler(k)
        if temp == 0:
            break
        accepted = incr < 0 or random.random() < math.exp(-incr / temp)
        if accepted:
            move.apply_move(s)
            if s.lb < best.lb:
                best = s.copy_solution()
        if record:
            history.append({"k": k, "temp": temp, "cost": s.lb})
        k += 1

    return (best, history) if record else best
