from roar_net_api.operations import (SupportsCopySolution,
                          SupportsLowerBound)
class Solution(SupportsCopySolution, SupportsLowerBound):
    def __init__(
        self,
        problem: "Problem",
        assignments: list[int],
        team_labels: list[list[dict[int, int]]],
        team_sizes: list[int],
        lb: int,
    ):
        self.problem = problem
        self.assignments = assignments
        self.team_labels = team_labels
        self.team_sizes = team_sizes
        self.lb = lb

    def objective_value(self) -> float:
        return self.lb
    
    def lower_bound(self) -> float:
        return self.lb


    def __eq__(self, other: Solution):
        return (self.problem     == other.problem     and 
                self.assignments == other.assignments and 
                self.team_labels == other.team_labels and 
                self.team_sizes  == other.team_sizes  and 
                self.lb          == other.lb)

    def __repr__(self): # repr for printing
        return (
            f"Solution(\n"
            f"  assignments={self.assignments!r},\n"
            #f"  num_students={len(self.assignments)}\n"
            f"  team_labels={self.team_labels!r},\n"
            f"  team_sizes={self.team_sizes!r},\n"
            #f"  num_teams={len(self.team_sizes)!r},\n"
            f"  cost={self.lb!r}\n"
            f")"
        )

    def copy_solution(self) -> Self: # copy
        return Solution(
            self.problem,
            self.assignments.copy(),
            [[d.copy() for d in row] for row in self.team_labels],
            self.team_sizes.copy(),
            self.lb,
        )

    def is_feasible(self) -> bool:
        if any(t == -1 for t in self.assignments):
            return False
        return all(
            self.problem.min_size <= s <= self.problem.max_size
            for s in self.team_sizes
        )