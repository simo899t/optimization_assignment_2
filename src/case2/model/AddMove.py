from roar_net_api.operations import (SupportsApplyMove, SupportsLowerBoundIncrement)
from .Solution import Solution

class AddMove(SupportsApplyMove[Solution], SupportsLowerBoundIncrement[Solution]):
    def __init__(self, student: int, toTeam: int):
        self.s = student
        self.toTeam = toTeam
    
    def objective_value_increment(self, solution: Solution) -> float:
        return self.lower_bound_increment(solution)
    
    def lower_bound_increment(self, solution: Solution) -> float:
        """
        Increments the lowerbound given a move (self)
        """ 
        p = solution.problem
        labels_count = solution.team_labels[self.toTeam]
        student_labels = p.attributes[self.s]
        incr = 0
        for a, label in enumerate(student_labels):
            if labels_count[a].get(label, 0) == 0:
                incr += p.weights[a]
        return incr

    def apply_move(self, solution: Solution) -> Solution:
        """
        Applies a move, and updates team_labels
        """
        solution.lb += self.lower_bound_increment(solution)
        solution.assignments[self.s] = self.toTeam
        solution.team_sizes[self.toTeam] += 1
        member_labels = solution.problem.attributes[self.s]
        for a, label in enumerate(member_labels):
            counts = solution.team_labels[self.toTeam][a]
            counts[label] = counts.get(label, 0) + 1
        return solution