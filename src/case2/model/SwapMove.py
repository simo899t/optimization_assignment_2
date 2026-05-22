from roar_net_api.operations import (SupportsApplyMove, SupportsObjectiveValueIncrement)
from .Solution import Solution

class SwapMove(SupportsApplyMove[Solution], SupportsObjectiveValueIncrement[Solution]):
    def __init__(self, student1: int, student2: int, team1: int, team2: int):
        self.s1 = student1
        self.s2 = student2
        self.t1 = team1
        self.t2 = team2

    def __str__(self):
        return f"swap student {self.s1} (team {self.t1}) with student {self.s2} (team {self.t2})"

    def objective_value_increment(self, solution: Solution) -> float:
        """
        Increments the lowerbound given a move (self)
        """ 
        prob = solution.problem
        t1_counts = solution.team_labels[self.t1]
        t2_counts = solution.team_labels[self.t2]
        s1_labels = prob.attributes[self.s1]
        s2_labels = prob.attributes[self.s2]
        incr = 0
        for a in range(len(s1_labels)):
            l1 = s1_labels[a]  # s1's label for attribute a
            l2 = s2_labels[a]  # s2's label for attribute a
            w = prob.weights[a]
            if l1 == l2:
                continue  # same label swapped in/out of each team — no net change
            # effect on t1: s1 leaves, s2 arrives
            if t1_counts[a].get(l1, 0) == 1:
                incr -= w  # last holder of l1 leaves t1
            if t1_counts[a].get(l2, 0) == 0:
                incr += w  # l2 is new to t1
            # effect on t2: s2 leaves, s1 arrives
            if t2_counts[a].get(l2, 0) == 1:
                incr -= w  # last holder of l2 leaves t2
            if t2_counts[a].get(l1, 0) == 0:
                incr += w  # l1 is new to t2
        return -incr

    def apply_move(self, solution: Solution) -> Solution:
        """
        Applies a move, and updates team_labels
        """
        prob = solution.problem
        solution.lb += self.objective_value_increment(solution)

        # s1 leaves t1, joins t2
        for a, label in enumerate(prob.attributes[self.s1]):
            from_counts = solution.team_labels[self.t1][a]
            from_counts[label] -= 1
            if from_counts[label] == 0:
                del from_counts[label]

            to_counts = solution.team_labels[self.t2][a]
            to_counts[label] = to_counts.get(label, 0) + 1
        
        solution.assignments[self.s1] = self.t2

        # s2 leaves t2, joins t1
        for a, label in enumerate(prob.attributes[self.s2]):
            from_counts = solution.team_labels[self.t2][a]
            from_counts[label] -= 1
            if from_counts[label] == 0:
                del from_counts[label]

            to_counts = solution.team_labels[self.t1][a]
            to_counts[label] = to_counts.get(label, 0) + 1
        
        solution.assignments[self.s2] = self.t1
        return solution
