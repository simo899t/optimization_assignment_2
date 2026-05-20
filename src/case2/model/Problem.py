from roar_net_api.operations import (SupportsConstructionNeighbourhood, 
                                     SupportsLocalNeighbourhood, 
                                     SupportsEmptySolution, 
                                     SupportsRandomSolution)
from typing import Self, TextIO
from .Solution import Solution
from .AddNeighbourhood import AddNeighbourhood
from .SwitchNeighbourhood import SwitchNeighbourhood
import random
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