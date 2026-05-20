from roar_net_api.operations import (SupportsApplyMove, SupportsObjectiveValueIncrement)
from .Solution import Solution

class Switch(SupportsApplyMove[Solution], SupportsObjectiveValueIncrement[Solution]):
    def __init__(self, student: int, toTeam: int, fromTeam: int):
        self.s = student
        self.toTeam = toTeam
        self.fromTeam = fromTeam

    def objective_value_increment(self, solution: Solution) -> float:
        return self.score_increment(solution)

    def score_increment(self, solution: Solution) -> float:
        prob = solution.problem
        from_counts = solution.team_labels[self.fromTeam]
        to_counts = solution.team_labels[self.toTeam]
        s_labels = prob.attributes[self.s]
        incr = 0
        for a, label in enumerate(s_labels):
            # s leaves fromTeam: lb drops if s was the last holder of this label
            if from_counts[a].get(label, 0) == 1:
                incr -= prob.weights[a]
            # s joins toTeam: lb rises if toTeam has no holder of this label yet
            if to_counts[a].get(label, 0) == 0:
                incr += prob.weights[a]
        return incr

    def apply_move(self, solution: Solution) -> Solution:
        prob = solution.problem

        for a, label in enumerate(prob.attributes[self.s]):
            from_counts = solution.team_labels[self.fromTeam][a]
            from_counts[label] -= 1
            if from_counts[label] == 0:
                solution.lb -= prob.weights[a]
                del from_counts[label]

            to_counts = solution.team_labels[self.toTeam][a]
            if to_counts.get(label, 0) == 0:
                solution.lb += prob.weights[a]
            to_counts[label] = to_counts.get(label, 0) + 1

        solution.assignments[self.s] = self.toTeam
        solution.team_sizes[self.fromTeam] -= 1
        solution.team_sizes[self.toTeam] += 1
        return solution