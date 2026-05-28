from roar_net_api.operations import (SupportsConstructionNeighbourhood, 
                                     SupportsLocalNeighbourhood, 
                                     SupportsEmptySolution, 
                                     SupportsRandomSolution)
from typing import Self, TextIO
from .Solution import Solution
from .AddNeighbourhood import AddNeighbourhood
from .SwapNeighbourhood import SwapNeighbourhood
import random
class Problem(
    SupportsConstructionNeighbourhood[AddNeighbourhood],
    SupportsLocalNeighbourhood[SwapNeighbourhood],
    SupportsEmptySolution[Solution],
    SupportsRandomSolution[Solution]):
    
    def __init__(
        self,
        n_students: int,
        n_teams: int,
        weights: list[int],
        attributes: list[list[int]],
        disagreements: list[tuple[int, int]],
        min_size: int,
        max_size: int,
    ):
        self.n_students = n_students
        self.n_teams = n_teams
        self.weights = weights
        self.attributes = attributes
        self.disagreements = disagreements
        self.min_size = min_size
        self.max_size = max_size

        # Initiate precomputed disagreement lists
        self.disagrees_with = [set() for _ in range(n_students)]
        for a, b in disagreements:
            self.disagrees_with[a].add(b)
            self.disagrees_with[b].add(a)

    def construction_neighbourhood(self, neighbourhoodType=None) -> AddNeighbourhood:
        return AddNeighbourhood(self, neighbourhoodType or "allFeasible")

    def local_neighbourhood(self) -> SwapNeighbourhood:
        return SwapNeighbourhood(self)
        
    def empty_solution(self) -> Solution:
        """
        Create as empty solution
        """        
        n_attributes = len(self.weights)
        return Solution(
            problem=self,
            assignments=[-1] * self.n_students,
            team_labels=[[dict() for _ in range(n_attributes)] for _ in range(self.n_teams)],
            team_sizes=[0] * self.n_teams,
            lb=0,
        )
    
    def random_solution(self) -> Solution:
        """
        Create as random feasible solution
        """
        n_attributes = len(self.weights)
        assignments = [-1] * self.n_students
        team_labels = [[dict() for _ in range(n_attributes)] for _ in range(self.n_teams)]
        team_sizes = [0] * self.n_teams
        lb = 0

        order = list(range(self.n_students))
        random.shuffle(order)

        for s in order:
            team_order = list(range(self.n_teams))
            random.shuffle(team_order)

            chosen = None
            for t in team_order:
                if team_sizes[t] >= self.max_size:
                    continue
                if any(assignments[other] == t for other in self.disagrees_with[s]):
                    continue
                chosen = t
                break

            if chosen is None:
                for t in team_order:
                    if team_sizes[t] < self.max_size:
                        chosen = t

            assignments[s] = chosen
            team_sizes[chosen] += 1
            for a, label in enumerate(self.attributes[s]):
                counts = team_labels[chosen][a]
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

        n_students, n_teams, n_attributes, n_disagreements, min_size, max_size = (
            int(x) for x in next_data_line()
        )

        weights = [int(x) for x in next_data_line()]
        if len(weights) != n_attributes:
            raise ValueError(
                f"Expected {n_attributes} attribute weights, got {len(weights)}"
            )

        attributes: list[list[int]] = []
        for _ in range(n_students):
            row = [int(x) for x in next_data_line()]
            if len(row) != n_attributes:
                raise ValueError(
                    f"Expected {n_attributes} attribute labels per students, got {len(row)}"
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
            n_students,
            n_teams,
            weights,
            attributes,
            disagreements,
            min_size,
            max_size
        )