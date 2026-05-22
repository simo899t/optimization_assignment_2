from __future__ import annotations
from typing import TYPE_CHECKING
from roar_net_api.operations import (SupportsMoves)
from collections.abc import Iterable
from .Solution import Solution
from .AddMove import AddMove
if TYPE_CHECKING:
    from .Problem import Problem

class AddNeighbourhood(SupportsMoves[Solution, AddMove]):
    def __init__(self, problem: "Problem", neighbourhoodType=None):
        self.problem = problem
        self.neighbourhoodType = neighbourhoodType

    def moves(self, solution: Solution) -> Iterable[AddMove]:
        """
        Calls the appropriate moves method
        """
        match (self.neighbourhoodType):
            case "minFirst":
                yield from self.minFirst(solution)
            
            case "mostDisagreementsFirst":
                yield from self.mostDisagreementsFirst(solution)

            case "hybridMoves":
                yield from self.hybridMoves(solution)

            case "allFeasible":
                yield from self.allFeasible(solution)

    def is_feasible_add(self, s: int, toTeam: int, solution: Solution) -> bool:
        """
        Returns true of the add move results in a feasible solution, otherwise false
        """
        prob = self.problem
        for c in prob.disagrees_with[s]:
            if solution.assignments[c] == toTeam:
                return False
        return True

    def minFirst(self, solution: Solution) -> Iterable[AddMove]:
        """
        Filters moves, such that moves which assigns students to one of the smallest teams are yielded first
        """
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


    def mostDisagreementsFirst(self, solution: Solution) -> Iterable[AddMove]:
        """
        Filters moves, such that moves that assigns the students with tho most amount of disagreements are yielded first
        """
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
        """
        Hybrid of mostDisagreementsFirst and minFirst
        """
        p = self.problem
        all_teams = range(p.n_teams)

        unassigned = [s for s, team in enumerate(solution.assignments) 
                      if team == -1]
        if not unassigned:
            return
        
        smallest = min(solution.team_sizes[t] for t in all_teams)
        candidate_teams = [t for t in all_teams if solution.team_sizes[t] == smallest]

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

    def allFeasible(self, solution: Solution) -> Iterable[AddMove]:
        """
        Returns all feasible swap moves
        """
        p = self.problem
        all_teams = range(p.n_teams)
        # students where their assignment is -1 (not assigned)
        unassigned = [s for s, team in enumerate(solution.assignments) 
                      if team == -1]
        if not unassigned:
            return # if no un assigned student, early exit
        
        under_min = [t for t in all_teams if solution.team_sizes[t] < p.min_size]
        if under_min:
            candidate_teams = under_min
        else:
            candidate_teams = [t for t in all_teams if solution.team_sizes[t] < p.max_size]


        for s in unassigned:
            teams = [t for t in candidate_teams if self.is_feasible_add(s, t, solution)]
            if not teams:
                teams = [t for t in all_teams if solution.team_sizes[t] < p.max_size and self.is_feasible_add(s, t, solution)]
            for t in teams:
                yield AddMove(s, t)