from __future__ import annotations
from typing import TYPE_CHECKING
from roar_net_api.operations import (SupportsMoves,SupportsRandomMovesWithoutReplacement,SupportsRandomMove)
from collections.abc import Iterable
from .Solution import Solution
from .SwapMove import SwapMove
import random
if TYPE_CHECKING:
    from .Problem import Problem

def sparse_fisher_yates_iter(n: int) -> Iterable[int]:
    p: dict[int, int] = dict()
    for i in range(n - 1, -1, -1):
        r = random.randrange(i + 1)
        yield p.get(r, r)
        if i != r:
            p[r] = p.get(i, i)


class SwapNeighbourhood(
    SupportsMoves[Solution, SwapMove],
    SupportsRandomMovesWithoutReplacement[Solution, SwapMove],
    SupportsRandomMove[Solution, SwapMove],
):
    def __init__(self, problem: "Problem"):
        self.problem = problem

    def moves(self, solution: Solution) -> Iterable[SwapMove]:
        """
        Returns all feasible swap moves
        """
        p = self.problem
        for s1 in range(p.n_students):
            for s2 in range(p.n_students):
                t1 = solution.assignments[s1]
                t2 = solution.assignments[s2]
                if t1 == t2:
                    continue
                if self._is_feasible_swap(s1, s2, t1, t2, solution):
                    yield SwapMove(s1, s2, t1, t2)

    def _is_feasible_swap(self, student1: int, student2: int, team1: int, team2: int, solution: Solution) -> bool:
        """
        Returns true if swap move results in a feasible solution, otherwise false
        """
        prob = self.problem
        for c in prob.disagrees_with[student1]:
            if c != student2 and solution.assignments[c] == team2:
                return False
        for c in prob.disagrees_with[student2]:
            if c != student1 and solution.assignments[c] == team1:
                return False
        return True
    
    def random_move(self, solution: Solution) -> SwapMove | None:
        return next(self.random_moves_without_replacement(solution), None)

    def random_moves_without_replacement(self, solution: Solution) -> Iterable[SwapMove]:
        """
        Creates random feasible moves
        """
        p = self.problem
        n = p.n_students
        total = n * n

        for idx in sparse_fisher_yates_iter(total):
            s1 = idx // n
            s2 = idx % n
            if s1 >= s2:
                continue
            
            t1, t2 = solution.assignments[s1], solution.assignments[s2]

            if t1 == t2:
                continue
            if self._is_feasible_switch(s1, s2, t1, t2, solution):
                yield SwapMove(s1, s2, t1, t2)