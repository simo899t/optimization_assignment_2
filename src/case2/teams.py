import math, random, time
from collections.abc import Iterable
from typing import Optional, Self, TextIO

from roar_net_api.operations import ( # Interface for the ROAR-NET-API
    SupportsCopySolution,
    SupportsObjectiveValue,
    SupportsLowerBound,
    SupportsConstructionNeighbourhood,
    SupportsLocalNeighbourhood,
    SupportsEmptySolution,
    SupportsRandomSolution,
    SupportsApplyMove,
    SupportsLowerBoundIncrement,
    SupportsObjectiveValueIncrement,
    SupportsMoves,
    SupportsRandomMovesWithoutReplacement,
    SupportsRandomMove,

)

# ---------------------------------- Helper ----------------------------------
def sparse_fisher_yates_iter(n: int) -> Iterable[int]:
    p: dict[int, int] = dict()
    for i in range(n - 1, -1, -1):
        r = random.randrange(i + 1)
        yield p.get(r, r)
        if i != r:
            p[r] = p.get(i, i)

# ---------------------------------- Solution ----------------------------------
class Solution(SupportsCopySolution, SupportsObjectiveValue, SupportsLowerBound):
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
            f"  team_labels={self.team_labels!r},\n"
            f"  team_sizes={self.team_sizes!r},\n"
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


# ---------------------------------- Moves ----------------------------------

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
        return -(cost + self.disagreementsHeuristic(solution))
    
    def disagreementsHeuristic(self, solution: Solution):
        weights = solution.problem.weights
        blocked = sum(1 for u in p.disagrees_with[self.s] if solution.assignments[u] == -1) #unassigned
        return blocked * (sum(weights))/len(weights)

    def apply_move(self, solution: Solution) -> Solution:
        solution.lb += self.lower_bound_increment(solution)
        solution.assignments[self.s] = self.toTeam
        solution.team_sizes[self.toTeam] += 1
        member_labels = solution.problem.attributes[self.s]
        for a, label in enumerate(member_labels):
            counts = solution.team_labels[self.toTeam][a]
            counts[label] = counts.get(label, 0) + 1
        return solution

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



# ---------------------------------- Neighbourhood ----------------------------------


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
                                        if len(p.disagrees_with[s])] == max_dis # only assign the students who has max number of disagreements
        
 
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
        
        # if any teams under min size, they should be filled first
        under_min = [team for team in all_teams if solution.team_sizes[team] < p.min_size]
        if under_min:
            candidate_teams = under_min
        else:
            # then choose the rest
            candidate_teams = [
                t for t in all_teams
                if solution.team_sizes[t] < p.max_size]
    
        candidate_teams = [
            t for t in candidate_teams
            if solution.team_sizes[t] <= p.max_size
        ]
    
        for s in unassigned:
            teams = [t for t in candidate_teams if self.is_feasible_add(s, t, solution)]
            if not teams:
                teams = [t for t in all_teams if solution.team_sizes[t] < p.max_size and self.is_feasible_add(s, t, solution)]
            for t in teams:
                yield AddMove(s, t)


class SwitchNeighbourhood(
    SupportsMoves[Solution, Switch],
    SupportsRandomMovesWithoutReplacement[Solution, Switch],
    SupportsRandomMove[Solution, Switch],
):
    def __init__(self, problem: "Problem", heuristic=None):
        self.problem = problem
        self.heuristic = heuristic
        assert self.heuristic in {"random", "balancedMoves", "labelMoves", "hybridMoves", "greedy"}, "please pick a heuristic for switchNeighbourhood"

    def moves(self, solution: Solution) -> Iterable[Switch]:
        match (self.heuristic):
            case "random":
                yield from self.randomMoves(solution)

            case "balancedMoves":
                yield from self.balancedMoves(solution)

            case "labelMoves":
                yield from self.labelMoves(solution)

            case "hybridMoves":
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
        total = p.n_members * (p.n_teams - 1)

        for iter in sparse_fisher_yates_iter(total):
            student = iter // (p.n_teams - 1)

            to_index = iter % (p.n_teams - 1)

            fromTeam = solution.assignments[student]

            # map 0..n_teams-2 to all teams except fromTeam
            toTeam = to_index
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

    def labelMoves(self, solution: Solution) -> Iterable[Switch]:
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

# ---------------------------------- Problem ----------------------------------

class Problem(
    SupportsConstructionNeighbourhood[AddNeighbourhood],
    SupportsLocalNeighbourhood[SwitchNeighbourhood],
    SupportsEmptySolution[Solution],
    SupportsRandomSolution[Solution]):
    
    def __init__(
        self,
        n_members: int,
        n_teams: int,
        weights: list[int],
        attributes: list[list[int]],
        disagreements: list[tuple[int, int]],
        min_size: int,
        max_size: int,
    ):
        self.n_members = n_members
        self.n_teams = n_teams
        self.weights = weights
        self.attributes = attributes
        self.disagreements = disagreements
        self.min_size = min_size
        self.max_size = max_size
        self.c_nbhood = None
        self.l_nbhood = None

        # precompute disagreement adjacency
        self.disagrees_with = [set() for _ in range(n_members)]
        for a, b in disagreements:
            self.disagrees_with[a].add(b)
            self.disagrees_with[b].add(a)

    def construction_neighbourhood(self, heuristic= "greedy") -> AddNeighbourhood:
        if self.c_nbhood is None:
            self.c_nbhood = AddNeighbourhood(self,heuristic)
        return self.c_nbhood

    def local_neighbourhood(self, heuristic="greedy") -> SwitchNeighbourhood:
        if self.l_nbhood is None:
            self.l_nbhood = SwitchNeighbourhood(self, heuristic)
        return self.l_nbhood

    def empty_solution(self) -> Solution:
        n_attributes = len(self.weights)
        return Solution(
            problem=self,
            assignments=[-1] * self.n_members,
            team_labels=[[dict() for _ in range(n_attributes)] for _ in range(self.n_teams)],
            team_sizes=[0] * self.n_teams,
            lb=0,
        )
    
    def random_solution(self) -> Solution:
        n_attributes = len(self.weights)
        assignments = [random.randrange(self.n_teams) for _ in range(self.n_members)]
        team_labels = [[dict() for _ in range(n_attributes)] for _ in range(self.n_teams)]
        team_sizes = [0] * self.n_teams
        lb = 0
        for member, team in enumerate(assignments):
            team_sizes[team] += 1
            for a, label in enumerate(self.attributes[member]):
                counts = team_labels[team][a]
                if counts.get(label, 0) == 0:
                    lb += self.weights[a]
                counts[label] = counts.get(label, 0) + 1
        
        return Solution(
            problem=self,
            assignments=assignments,
            team_labels=team_labels,
            team_sizes=team_sizes,
            lb=lb,
        )
    
    def worst_solution(self) -> Solution:
        n_attributes = len(self.weights)

        assignments = [0] * self.n_members

        team_labels = [[dict() for _ in
                         range(n_attributes)] for _ in range(self.n_teams)]
        team_sizes = [0] * self.n_teams

        lb = 0

        for member in range(self.n_members):
            team_sizes[0] += 1
            for a, label in enumerate(self.attributes[member]):
                counts = team_labels[0][a]
                if counts.get(label, 0) == 0:
                    lb += self.weights[a]
                counts[label] = counts.get(label, 0) + 1

        return Solution(
            problem=self,
            assignments=assignments,
            team_labels=team_labels,
            team_sizes=team_sizes,
            lb=lb,
        )

    @classmethod
    def from_textIO(cls, f: TextIO) -> Self:
        """
        Create a problem from a text I/O source `f`
        """
        def next_data_line() -> list[str]:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    return stripped.split()
            raise ValueError("Unexpected end of input")

        n_members, n_teams, n_attributes, n_disagreements, min_size, max_size = (
            int(x) for x in next_data_line()
        )

        weights = [int(x) for x in next_data_line()]
        if len(weights) != n_attributes:
            raise ValueError(
                f"Expected {n_attributes} attribute weights, got {len(weights)}"
            )

        attributes: list[list[int]] = []
        for _ in range(n_members):
            row = [int(x) for x in next_data_line()]
            if len(row) != n_attributes:
                raise ValueError(
                    f"Expected {n_attributes} attribute labels per member, got {len(row)}"
                )
            attributes.append(row)

        disagreements: list[tuple[int, int]] = []
        for _ in range(n_disagreements):
            tokens = next_data_line()
            if len(tokens) != 2:
                raise ValueError(f"Expected 2 ids per disagreement, got {len(tokens)}")
            a, b = int(tokens[0]), int(tokens[1])
            disagreements.append((a, b))

        return cls(
            n_members,
            n_teams,
            weights,
            attributes,
            disagreements,
            min_size,
            max_size
        )

if __name__ == "__main__":
    import roar_net_api.algorithms as alg
    
    name = "teams optimization task"
    t0 = time.time()
    # Read from file if provided, otherwise stdin

    instance = (
        "tfp_13n_3q_4l_5u_3a_5d.txt"
        #"tfp_131n_27q_4l_5u_10a_10d.txt"
        #"tfp_200n_40q_5l_5u_10a_15d.txt"
        #"tfp_300n_60q_5l_5u_10a_40d.txt"
        )

    with open(instance) as file:
        p = Problem.from_textIO(file)

    c_heuristic = (
        #"balanced"
        "constrained"
        #"hybrid"
        #"greedy"
        )

    p.construction_neighbourhood(c_heuristic)

    #print("empty solution")
    #s = p.empty_solution()

    #s = p.worst_solution()

    #print("random")
    s = p.random_solution()

    print(f"{c_heuristic} constructed solution")
    #s = alg.greedy_construction(p)
    s = alg.beam_search(p)
    #s = alg.grasp(p, budget=10) <- wont work :(

    print(s)

    #print(s)
    l_heuristic = (
        #"random"
        #"constrained"
        #"hybrid"
        "greedy"
        )
    
    p.local_neighbourhood(l_heuristic)

    t0 = time.time()
    print(f"{l_heuristic} improvement solution")
    #s = alg.best_improvement(p, s)
    s = alg.first_improvement(p,s)
    #s = alg.sa(p, s, budget=5.0, init_temp=50.0)

    print(s)
    print(f"Is feasible: {s.is_feasible()}")
    print(f"Execution time: {time.time()-t0}")
    with open("solution.sol", "w") as out:
        out.write(" ".join(str(t) for t in s.assignments) + "\n")