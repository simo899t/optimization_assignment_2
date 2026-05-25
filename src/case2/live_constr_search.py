#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Andreia P. Guerreiro <andreia.guerreiro@tecnico.ulisboa.pt>
#
# SPDX-License-Identifier: Apache-2.0

#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tabulate import tabulate
import math


# In[25]:


class Problem:
    
    def __init__(self, mx):
        self.mx = mx
        self.sz = len(self.mx)
        
        self.ub = 0
        for i in range(self.sz):
            self.ub += sum([x for x in self.mx[i][i+1:] if x > 0])
        
    def __str__(self):
        return f"{tabulate(self.mx)}\nUB: {self.ub}"
    
    def empty_solution(self):
        return Solution(self, [], 0, self.ub)
        
    def construction_neighbourhood(self):
        return AddNeighbourhood(self)
        
    @classmethod
    def from_textio(cls, f):
        n = int(f.readline())
        
        mx = [n*[0] for _ in range(n)]
        L = map(int, f.read().split())
        for i in range(n):
            for j in range(i, n):
                mx[i][j] = mx[j][i] = next(L)
        return cls(mx)


# In[26]:


f = open("./mycliques.txt")
p = Problem.from_textio(f)
f.close()
print(f"-- Problem --\n{p}")


# In[54]:


class Solution:
    def __init__(self, problem, clique, k, ub):
        self.problem = problem
        self.clique = clique
        self.k = k
        self.ub = ub
        
    def __str__(self):
        return f"\tclique: {self.clique}\n\tk: {self.k}\n\tUB: {self.ub}"
        
    def copy_solution(self):
        return Solution(self.problem, self.clique.copy(), self.k, self.ub)
        
    def objective_value(self):
        if len(self.clique) == self.problem.sz:
            return -self.ub
        return None
    
    def lower_bound(self):
        return -self.ub


# In[28]:


s = p.empty_solution()
print(f"Empty solution\n{s}")


# In[29]:


class AddNeighbourhood:
    def __init__(self, problem):
        self.problem = problem
        
    def moves(self, solution):
        v = len(solution.clique)
        if v < self.problem.sz:
            for c in range(solution.k+1):
                yield AddMove(self, v, c)
        


# In[48]:


class AddMove:
    def __init__(self, neighbourhood, v, c):
        self.neighbourhood = neighbourhood
        self.v = v
        self.c = c
        self.ub_incr = None
        
    def __str__(self):
        return f"add node {self.v} to clique {self.c}"
    
    def lower_bound_increment(self, solution):
        return -self._upper_bound_increment(solution)
        
    def apply_move(self, solution):
        solution.ub += self._upper_bound_increment(solution)
        
        if self.c == solution.k: # new clique
            solution.k += 1
        solution.clique.append(self.c)


# In[49]:


constr_rule = p.construction_neighbourhood()
s = p.empty_solution()
moves = constr_rule.moves(s)
m = next(moves)
print(f"First move: {m}")

#%%

m.apply_move(s)
print(f"Partial solution:\n{s}")
for m in constr_rule.moves(s):
    print(f"Allowed move: {m}")


# In[56]:


constr_rule = p.construction_neighbourhood()
s = p.empty_solution()
s0 = s.copy_solution()
while True:
    best_move, best_incr = None, math.inf
    moves = constr_rule.moves(s)
    for move in moves:
        incr = move.lower_bound_increment(s)
        if incr is not None and incr < best_incr:
            best_move, best_incr = move, incr
            if incr == 0:
                break
    if best_move is None:
        break
    print(f"best move: {best_move}")
    best_move.apply_move(s)
    print(f"s: {s}\n")

        
print(f"\n-- Greedy solution --\n{s}")
print(f"Objective value: {s.objective_value()}")

print(f"empty solution: {s0}")
        
        
    



# %%
