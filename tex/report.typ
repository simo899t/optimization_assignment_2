#import "temp/temp.typ": *

// ─── Settings ────────────────────────────────────────────────────────────────
#let courseid   = "AI505"
#let coursename = "Optimization"
#let term       = "Spring 2026"
#let dept       = "Department of Mathematics and Computer Science"
#let university = "University of Southern Denmark, Odense"
#let authors    = "Simon Holm, Johannes Rothe"
#let assnr      = "2"
#show: code-style

// ─── Page layout ─────────────────────────────────────────────────────────────
#set page(
  paper: "a4",
  margin: 2.7cm,
  header: context {
    set text(size: 10pt)
    if counter(page).get().first() == 1 {
      grid(
        columns: (1fr, auto),
        align: (left + horizon, right + horizon),
        [#dept \ #university],
        [29 May 2026 \ #authors],
      )
      v(-6pt)
      line(length: 100%, stroke: 0.4pt)
    } else {
      align(right)[#authors]
      v(-6pt)
      line(length: 100%, stroke: 0.4pt)
    }
  },
  footer: context {
    line(length: 100%, stroke: 0.4pt)
    v(-6pt)
    align(center)[
      #set text(size: 10pt)
      Page #counter(page).display() of #counter(page).final().first()
    ]
  },
)

// ─── Typography ───────────────────────────────────────────────────────────────
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify:true,leading: 0.65em, spacing: 2em, first-line-indent: 0pt)

// Number equations
#set math.equation(numbering: "(1)")

// Section numbering
//#set heading(numbering: "1.1")

// ─── Algorithm block helper ───────────────────────────────────────────────────
#let algorithm(caption: none, body) = {
  set text(size: 10pt)
  block(
    width: 100%,
    stroke: (top: 1pt, bottom: 1pt),
    inset: (x: 8pt, y: 6pt),
  )[
    #if caption != none [
      *Algorithm:* #caption \
      #line(length: 100%, stroke: 0.4pt)
      #v(-16pt)
    ]
    #body
  ]
}

// ─── Title ────────────────────────────────────────────────────────────────────
#v(-4pt)
#align(left)[
  #text(size: 11pt)[#courseid -- #coursename]
  #v(0.2cm)
  #text(size: 14pt, weight: "bold")[
    Answers to Obligatory Assignment #assnr, Spring 2026
  ]
  #v(0.4em)
  #line(length: 100%, stroke: 0.8pt)
]


// ─── Case 1 ───────────────────────────────────────────────────────────────────
#pagebreak()
= Case 1
Let $ P = {x in RR^n | tran(bold(a)_i) x <= b_i, i = 1, dots, m  } $
be a nonempty, bounded polyhedron with nonempty interior.

== Task 1 - Defining the center
The center of $P$ is defined by a minimization problem over the objective function:
$ min_x f(x)  st g(x) <= 0 $
Which is found be rewriting the linear constraint $tran(bold(a))_i bold(x) <= b_i$ to $s_i =b_i - tran(bold(a))_i bold(x)$ so the variable $s_i$ describes the slack, or distance to the barrier. 

where $g_i (bold(x)) = tran(bold(a))_i bold(x) -b_i$ describes the slack, or distance to the barrier


Lets rewrite the objective function using the standard log barrier:$ phi_rho (bold(x)) =f(bold(x))+ phi(bold(x)) $ 
where $phi (bold(x)) =- sum_i log(-g_i (bold(x)))$

This minimization problem ensures that steps towards a barrier is penalized, and thus finding a minimum $x^*$ (as far away from any barrier) will be an approximation of the center

The objective function, while penalizing proximity to constraint boundaries (barriers), diverges to $oo$ as $-log(-g(bold(x))) -> oo$ as $g(bold(x)) to 0$.

== Task 2 - Analytical properties

// ─── Case 2 ───────────────────────────────────────────────────────────────────
#pagebreak()
= Case 2
In this case the objective is to fairly distributes students across teams such that their attributes match the most. As each attribute carry a weight to determine its importance. 

== Task 1
This can be modeled as a Integer Linear Programming (ILP) problem.

Given the objective function
$ sum_(T in cal(T)) sum_(a in A) w(a)z_(T,a) = sum_(T in cal(T)) sum_(a in A)sum_(b in L_a) w(a)y_(T,a,b) $

Then task is to minimize $sum_(T in cal(T)) sum_(a in A)sum_(b in L_a) w(a)y_(T,a,b)$

Lets go over the different constraints for this problem
1. Each student can only be assigned to exactly 1 team
$ sum_(T in cal(T)) x_(s,T) = 1 quad forall s in S $

2. The size of a team is limited to $ell <= |T| <= u$ 
$ ell <= sum_(s in S) x_(s,T) <= u quad forall T in cal(T) $

3. Two student who share a disagreement, must not be on the same team
$ x_(s_1,T) + x_(s_2,T) <= 1 quad forall (s_1,s_2) in D, forall T in cal(T) $



And so one can define the minimization task as the following:

$ min  sum_(T in cal(T)) sum_(a in A)sum_(b in L_a) w(a)y_(T,a,b)\
st #align($

sum_(T in cal(T)) x_s = 1 quad &forall s in S \

ell <= sum_(s in S) x_s <= u quad &forall T in cal(T) \

x_(s_1,T) + x_(s_2,T) <= 1 quad &forall (s_1,s_2) in D, forall T in cal(T)\

x_(s,T), y_(T,a,b) in {0,1} quad &$) $


#pagebreak()
= Case 2 (cont.)
Task 2, 3 and 4 all implement the `ROAR-NET-API`. This allows using highly optimized construction and search functions like `greedy_construction` and `beam_search`. Since `ROAR-NET-API` is an external framework, is expects a problem to implement certain interfaces like: `SupportsLowerBound` or `SupportsApplyMove`. These interfaces define how the framework can interact with the problem without knowing the specific problem details. 

By using `ROAR-NET-API` one can focus on implementing classes for the Problem, Solution, Move, and Neighbourhood, while the framework handles the search process. Because of this the development process is split into 3 tasks.
1. Solution construction (Task 2)
2. Solution improvement (Task 3)
3. Meta-heuristics (Task 4)

== Task 2
Lets define problem and implement a solution construction, such that the `ROAR-NET-API` can use it. 

This is done by
1. Defining the problem
2. Define the solution
3. Search for valid moves
4. Initialize the problem iteratively with valid moves


The problem needs a class for defining the problem itself.
```py
class Problem(...):
    def __init__(...):
        self.n_members = n_members
        self.n_teams = n_teams
        self.weights = weights
        self.attributes = attributes
        self.disagreements = disagreements
        self.min_size = min_size
        self.max_size = max_size
```<problem11>
The problem should by use of the method ```py from_textIO(cls, f: textIO)``` translate the `instance` to a problem which is readable from the `ROAR-NET-API`.

#pagebreak()
The problem should moreover initialize the both the neighbourhood and lists a list of sets to map disagreements for each student. This way the algorithm can always see for any student which other students are in disagreements.
#codly(offset-from: <problem11>, smart-indent: true)
```py
        self.c_nbhood = None
        self.l_nbhood = None
        self.disagrees_with: list[set[int]] = [set() for _ in range(n_members)]
        for a, b in disagreements:
            self.disagrees_with[a].add(b)
            self.disagrees_with[b].add(a)
```
After the problem definition, its also important that the solution is defined. The solution should contain: a reference to the problem instance (so the solution can access problem data), a list of assignments, the labels within each team in the solution, the team sizes, and the lower bound. Now that the problem is well defined, one can create an empty solution. The `empty_solution`  is then just an instance of a solution with empty teams and a lower bound of 0.
Now one can represent the problem as a solution (though an empty one) by `print(Problem.from_textIO(file).empty_solution())`
```
Solution(
  assignments=[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
  team_labels=[[{}, {}, {}], [{}, {}, {}], [{}, {}, {}]],
  team_sizes=[0, 0, 0],
  lb=0
)
```
Notice how team asignments are labeled as `-1`, meaning that all students are unassigned.

For the improvement task, its more optimal for the solution to be initialized in some greedy suboptimal way, rather than fully unsigned. For this one can use the `roar_net_api.algorithms.greedy_construction()`. Methods like this one needs class methods to implement `SupportsConstructionNeighbourhood` and `SupportsMoves`. This class should create a neighborhood of moves which the algorithm can take. 


```py
def moves(self, solution: Solution) -> Iterable[AddMove]:
        p = self.problem
        # students where their assignment is -1 (not assigned)
        unassigned = [s for s, team in enumerate(solution.assignments) 
                      if team == -1]
        if not unassigned:
            return # if no un assigned student, early exit
```
```
        # if any teams under min size, they should be filled first
        under_min = [team for team in range(p.n_teams) if solution.team_sizes[team] < p.min_size]
        if under_min:
            candidate_teams = under_min
        else:
            # then choose the rest
            candidate_teams = [
                t for t in range(p.n_teams)
                if solution.team_sizes[t] < p.max_size]
```
```
        for s in unassigned: # for each unassigned student
            blocked_teams = {  # which teams s go in (by disagreements)
                solution.assignments[c]
                for c in p.disagrees_with[s]
                if solution.assignments[c] != -1
            }
            for t in candidate_teams:
                if t not in blocked_teams: # if team is not blocked, yield move
                    yield AddMove(self, s, t)
```
The `moves` function above iterates through the unassigned students, and shou

#pagebreak()


```
Solution(
  assignments=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, -1, -1],
  team_labels=[[{1: 3, 0: 1}, {5: 1, 7: 1, 1: 2}, {2: 2, 1: 2}], 
    [{0: 2, 1: 2}, {5: 3, 7: 1}, {3: 2, 0: 1, 1: 1}], 
    [{0: 2, 1: 1}, {1: 1, 0: 1, 4: 1}, {0: 1, 3: 1, 1: 1}]],
  team_sizes=[4, 4, 3],
  lb=420
)
```


== Task 3



== Task 4
// ─── Appendix ─────────────────────────────────────────────────────────────────
#pagebreak()
#bib("references.bib")
