from __future__ import annotations
from typing import TYPE_CHECKING
from roar_net_api.operations import (SupportsMoves)
from collections.abc import Iterable
from .Solution import Solution
from .AddMove import AddMove
if TYPE_CHECKING:
    from .Problem import Problem
class AddNeighbourhood(SupportsMoves[Solution, AddMove]):
    def __init__(self, problem: "Problem", heuristic=None):
        self.problem = problem
        self.heuristic = heuristic
        assert heuristic in {"balanced", "constrained", "hybrid", "greedy"}, "please pick a heuristic"

    def moves(self, solution: Solution) -> Iterable[AddMove]:
        match (self.heuristic):
            case "balanced":
                yield from self.balancedMoves(solution)
            
            case "constrained":
                yield from self.constraintMoves(solution)

            case "hybrid":
                yield from self.hybridMoves(solution)

            case "greedy":
                yield from self.greedyMoves(solution)

    def is_feasible_add(self, s: int, toTeam: int, solution: Solution) -> bool:
        prob = self.problem
        for c in prob.disagrees_with[s]:
            if solution.assignments[c] == toTeam:
                return False
        return True

    def balancedMoves(self, solution: Solution) -> Iterable[AddMove]:
        p = self.problem
        all_teams = range(p.n_teams)

        # students where their assignment is -1 (not assigned)
        unassigned = [s for s, team in enumerate(solution.assignments) if team == -1]
        if not unassigned:
            return # if no un assigned student, early exit

        smallest = min(solution.team_sizes[t] for t in all_teams)
        candidate_teams = [t for t in all_teams if solution.team_sizes[t] == smallest]

        for s in unassigned:
            teams = [t for t in candidate_teams if self.is_feasible_add(s, t, solution)]
            if not teams:
                teams = [t for t in all_teams if solution.team_sizes[t] < p.max_size and self.is_feasible_add(s, t, solution)]
            for t in teams:
                yield AddMove(s, t)


    def constraintMoves(self, solution: Solution) -> Iterable[AddMove]:
        p = self.problem
        all_teams = range(p.n_teams)
        # students where their assignment is -1 (not assigned)
        unassigned = [s for s, team in enumerate(solution.assignments) if team == -1]
        # print(f"constraintMoves: unassigned={unassigned}, sizes={solution.team_sizes}")

        if not unassigned:
            return # if no un assigned student, early exit

        max_dis = max(len(p.disagrees_with[s])for s in unassigned) # save the number of max disagreements for a student
        unassigned_priority_students = [s for s in unassigned
                                        if len(p.disagrees_with[s]) == max_dis] # only assign the students who has max number of disagreements
        
 
        candidate_teams = [t for t in all_teams if solution.team_sizes[t] < p.max_size]

        for s in unassigned_priority_students:
            for t in candidate_teams:
                if self.is_feasible_add(s, t, solution):
                    yield AddMove(s, t)

    def hybridMoves(self, solution: Solution) -> Iterable[AddMove]:
        p = self.problem
        all_teams = range(p.n_teams)

        unassigned = [s for s, team in enumerate(solution.assignments) 
                      if team == -1]
        if not unassigned:
            return
        
        smallest = min(solution.team_sizes[t] for t in all_teams)
        candidate_teams = [t for t in all_teams if solution.team_sizes[t] == smallest]

        if not candidate_teams:
            candidate_teams = [
                t for t in all_teams
                if solution.team_sizes[t] < p.max_size
            ]

        max_dis = max(len(p.disagrees_with[s])for s in unassigned) # save the number of max disagreements for a student
        unassigned_priority_students = [
        s for s in unassigned
        if len(p.disagrees_with[s]) == max_dis # only assign the students who has max number of disagreements
        ]

        for s in unassigned_priority_students:
            teams = [t for t in candidate_teams if self.is_feasible_add(s, t, solution)]
            if not teams:
                teams = [t for t in all_teams if solution.team_sizes[t] < p.max_size and self.is_feasible_add(s, t, solution)]
            for t in teams:
                yield AddMove(s, t)

    def greedyMoves(self, solution: Solution) -> Iterable[AddMove]:
        p = self.problem
        all_teams = range(p.n_teams)
        # students where their assignment is -1 (not assigned)
        unassigned = [s for s, team in enumerate(solution.assignments) 
                      if team == -1]
        if not unassigned:
            return # if no un assigned student, early exit
        
        under_min = [t for t in all_teams if solution.team_sizes[t] < p.min_size]
        candidate_teams = under_min if under_min else [t for t in all_teams if solution.team_sizes[t] < p.max_size]

    
        for s in unassigned:
            teams = [t for t in candidate_teams if self.is_feasible_add(s, t, solution)]
            if not teams:
                teams = [t for t in all_teams if solution.team_sizes[t] < p.max_size and self.is_feasible_add(s, t, solution)]
            for t in teams:
                yield AddMove(s, t)