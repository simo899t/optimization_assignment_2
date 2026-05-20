from __future__ import annotations
from typing import TYPE_CHECKING
from roar_net_api.operations import (SupportsMoves,SupportsRandomMovesWithoutReplacement,SupportsRandomMove)
from collections.abc import Iterable
from .Solution import Solution
from .Switch import Switch
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

class SwitchNeighbourhood(
    SupportsMoves[Solution, Switch],
    SupportsRandomMovesWithoutReplacement[Solution, Switch],
    SupportsRandomMove[Solution, Switch],
):
    def __init__(self, problem: "Problem", heuristic=None):
        self.problem = problem
        self.heuristic = heuristic
        assert self.heuristic in {"random", "balanced", "constrained", "hybrid", "greedy"}, "please pick a heuristic for switchNeighbourhood"

    def moves(self, solution: Solution) -> Iterable[Switch]:
        match (self.heuristic):
            case "random":
                yield from self.randomMoves(solution)

            case "balanced":
                yield from self.balancedMoves(solution)

            case "constrained":
                yield from self.constraintMoves(solution)

            case "hybrid":
                yield from self.hybridMoves(solution)

            case "greedy":
                yield from self.greedyMoves(solution)

    def _is_feasible_switch(self, s: int, toTeam: int, solution: Solution) -> bool:
        prob = self.problem
        for c in prob.disagrees_with[s]:
            if solution.assignments[c] == toTeam:
                return False
        return True
    
    def randomMoves(self, solution: Solution) -> Iterable[Switch]:
        yield from self.random_moves_without_replacement(solution)

    def random_moves_without_replacement(self, solution: Solution) -> Iterable[Switch]:
        p = self.problem
        valid_teams = p.n_teams - 1
        total = p.n_members * valid_teams

        if p.n_teams <= 1:
            return # <- early exit
        for iter in sparse_fisher_yates_iter(total):
            student = iter // valid_teams

            toTeam = iter % valid_teams

            fromTeam = solution.assignments[student]

            # map 0..n_teams-2 to all teams except fromTeam
            if toTeam >= fromTeam:
                toTeam += 1

            if solution.team_sizes[fromTeam] - 1 < p.min_size:
                continue
            if solution.team_sizes[toTeam] + 1 > p.max_size:
                continue
            if not self._is_feasible_switch(student, toTeam, solution):
                continue

            yield Switch(student, toTeam, fromTeam)

    def balancedMoves(self, solution: Solution) -> Iterable[Switch]:
        pass

    def constraintMoves(self, solution: Solution) -> Iterable[Switch]:
        pass

    def hybridMoves(self, solution: Solution) -> Iterable[Switch]:
        pass

    def greedyMoves(self, solution: Solution) -> Iterable[Switch]:
        p = self.problem
        for s in range(p.n_members):
            fromTeam = solution.assignments[s]
            for toTeam in range(p.n_teams):
                if toTeam == fromTeam:
                    continue
                if solution.team_sizes[fromTeam] - 1 < p.min_size:
                    continue
                if solution.team_sizes[toTeam] + 1 > p.max_size:
                    continue
                if self._is_feasible_switch(s, toTeam, solution):
                    yield Switch(s, toTeam, fromTeam)