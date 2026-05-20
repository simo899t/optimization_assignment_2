from roar_net_api.operations import (SupportsApplyMove, SupportsLowerBoundIncrement)
from .Solution import Solution

class AddMove(SupportsApplyMove[Solution], SupportsLowerBoundIncrement[Solution]):
    def __init__(self, student: int, toTeam: int):
        self.s = student
        self.toTeam = toTeam

    def score_increment(self, solution: Solution) -> float:
        p = solution.problem
        labels_count = solution.team_labels[self.toTeam]
        student_labels = p.attributes[self.s]
        incr = 0
        for a, label in enumerate(student_labels):
            if labels_count[a].get(label, 0) == 0:
                incr += p.weights[a]
        return incr
    
    def objective_value_increment(self, solution: Solution) -> float:
        return self.score_increment(solution)
    
    def lower_bound_increment(self, solution: Solution) -> float:
        cost = self.score_increment(solution)
        #return -(cost + self.disagreementsHeuristic(solution) + self.teamBalanceHeuristic(solution))
        #return -(cost + self.disagreementsHeuristic(solution))
        return -(cost + self.teamBalanceHeuristic(solution))
        #return -cost
    
    def disagreementsHeuristic(self, solution: Solution) -> float:
        p = solution.problem
        blocked = sum(1 for u in p.disagrees_with[self.s] if solution.assignments[u] == -1) #unassigned
        mu = 1
        scale = mu * sum(p.weights) / len(p.weights)
        return blocked * scale
    
    def teamBalanceHeuristic(self, solution: Solution) -> float:
        p = solution.problem
        mu = 1
        scale = mu * sum(p.weights) / len(p.weights)
        smallest = min(solution.team_sizes)
        return -(solution.team_sizes[self.toTeam] - smallest) * scale

    def apply_move(self, solution: Solution) -> Solution:
        solution.lb += self.score_increment(solution)
        solution.assignments[self.s] = self.toTeam
        solution.team_sizes[self.toTeam] += 1
        member_labels = solution.problem.attributes[self.s]
        for a, label in enumerate(member_labels):
            counts = solution.team_labels[self.toTeam][a]
            counts[label] = counts.get(label, 0) + 1
        return solution