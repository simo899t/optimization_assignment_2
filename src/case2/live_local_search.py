#!/usr/bin/env python
# coding: utf-8

# <!--
# SPDX-FileCopyrightText: 2025 Andreia P. Guerreiro <andreia.guerreiro@tecnico.ulisboa.pt>
# 
# SPDX-License-Identifier: Apache-2.0
# -->

# In[1]:


from tabulate import tabulate
import math
import copy
import random


# In[2]:


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
        unused = list(range(self.sz-1,-1,-1))
        return Solution(self, [], {}, unused, 0, self.ub)
        
    def construction_neighbourhood(self):
        return AddNeighbourhood(self)
    
    def local_neighbourhood(self):
        return LocalNeighbourhood(self)
    
    def random_solution(self):
        kmax = random.randint(1, self.sz)
        clique = [-1 for v in range(self.sz)]
        nodes = {}
        k = 0
        ub = 0
        
        for v in range(self.sz):
            c = random.randint(0, kmax-1)
            if c >= k: # new clique
                c = k
                k += 1
                nodes[c] = set()
            clique[v] = c
            for v2 in nodes[c]:
                ub += self.mx[v][v2]
            nodes[c].add(v)
        unused = list(range(self.sz-1, k-1, -1))
        
        return Solution(self, clique, nodes, unused, k, ub)
        
    @classmethod
    def from_textio(cls, f):
        n = int(f.readline())
        
        mx = [n*[0] for _ in range(n)]
        L = map(int, f.read().split())
        for i in range(n):
            for j in range(i, n):
                mx[i][j] = mx[j][i] = next(L)
        return cls(mx)


# In[3]:


f = open("./mycliques.txt")
p = Problem.from_textio(f)
f.close()
print(f"-- Problem --\n{p}")


# In[4]:


class Solution:
    def __init__(self, problem, clique, nodes, unused, k, ub):
        self.problem = problem
        self.clique = clique
        self.nodes = nodes
        self.unused = unused
        self.k = k
        self.ub = ub
        
    def __str__(self):
        nodes = "\n".join([f"\t\t{k}: {str(v)}" for (k,v) in self.nodes.items()])
        return f"\tclique: {self.clique}\n\tnodes:\n{nodes}\n\tunused:{self.unused}\n\tk: {self.k}\n\tUB: {self.ub}"
        
    def copy_solution(self):
        return Solution(self.problem, self.clique.copy(), copy.deepcopy(self.nodes), self.unused.copy(), self.k, self.ub)
        
    def objective_value(self):
        if len(self.clique) == self.problem.sz:
            return -self.ub
        return None
    
    def lower_bound(self):
        return -self.ub
    
    


# In[5]:


s = p.empty_solution()
print(f"Empty solution\n{s}")


# In[6]:


s = p.random_solution()
print(f"\n-- Random solution --\n{s}")


# In[7]:


class AddNeighbourhood:
    def __init__(self, problem):
        self.problem = problem
        
    def moves(self, solution):
        v = len(solution.clique)
        if v < self.problem.sz:
            for c in range(solution.k+1):
                yield AddMove(self, v, c)
        


# In[8]:


class AddMove:
    def __init__(self, neighbourhood, v, c):
        self.neighbourhood = neighbourhood
        self.v = v
        self.c = c
        self.ub_incr = None
        
    def __str__(self):
        return f"add node {self.v} to clique {self.c}"
    
    def _upper_bound_increment(self, solution):
        assert self.v == len(solution.clique) and self.c <= solution.k
        
        if self.ub_incr is None:
            self.ub_incr = 0
            for v in range(len(solution.clique)):
                w = solution.problem.mx[v][self.v]
                if solution.clique[v] == self.c and w < 0:
                    self.ub_incr += w
                elif solution.clique[v] != self.c and w > 0:
                    self.ub_incr -= w
        return self.ub_incr
    
    def lower_bound_increment(self, solution):
        return -self._upper_bound_increment(solution)
        
    def apply_move(self, solution):
        solution.ub += self._upper_bound_increment(solution)
        
        if self.c == solution.k: # new clique
            solution.k += 1
            c = solution.unused.pop()
            assert c == self.c
            solution.nodes[c] = set()
        solution.clique.append(self.c)
        solution.nodes[self.c].add(self.v)


# In[9]:


constr_rule = p.construction_neighbourhood()
s = p.empty_solution()
moves = constr_rule.moves(s)
m = next(moves)
print(f"First move: {m}")

m.apply_move(s)
print(f"Partial solution:\n{s}")
for m in constr_rule.moves(s):
    print(f"Allowed move: {m}")


# In[11]:


def greedy_algorithm(p):
    constr_rule = p.construction_neighbourhood()
    s = p.empty_solution()
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
        #print(f"best move: {best_move}")
        best_move.apply_move(s)
        #print(f"s: {s}\n")
    return s


# In[12]:


gs = greedy_algorithm(p)
print(f"\n-- Greedy solution --\n{gs}")
print(f"Objective value: {gs.objective_value()}")


# In[ ]:


class LocalNeighbourhood:
    def __init__(self, problem):
        self.problem = problem
        
    def moves(self, solution):
        for v in range(self.problem.sz):
            cv = solution.clique[v]
            cv_sz = len(solution.nodes[cv])
            for c in solution.nodes.keys():
                if cv != c:
                    if cv_sz == 1 and len(solution.nodes[c]) == 1 and cv < c:
                        continue
                    yield LocalMove(self,v,c)
            if cv_sz > 2 or (cv_sz == 2 and v == max(solution.nodes[cv])):
                yield LocalMove(self, v, solution.unused[-1])


# In[ ]:


class LocalMove:
    def __init__(self, neighbourhood, v, c):
        self.neighbourhood = neighbourhood
        self.v = v
        self.c = c
        self.ov_incr = None
        
    def __str__(self):
        return f"add node {self.v} to clique {self.c}"
    
    def objective_value_increment(self, solution):
        assert len(solution.clique) == solution.problem.sz #and 0 <= self.v <= len(s)
        
        if self.ov_incr is None:
            self.ov_incr = 0
            cv = solution.clique[self.v]
            for v in solution.nodes[cv]:
                self.ov_incr -= solution.problem.mx[self.v][v]
            if self.c in solution.nodes:
                for v in solution.nodes[self.c]:
                    self.ov_incr += solution.problem.mx[self.v][v]
        return -self.ov_incr
    
    def apply_move(self, solution):
        solution.ub += -self.objective_value_increment(solution)
        
        cv = solution.clique[self.v]
        solution.nodes[cv].remove(self.v)
        
        if self.c not in solution.nodes:
            solution.k += 1
            cnext = solution.unused.pop()
            assert cnext == self.c
            solution.nodes[self.c] = set()
            
        if len(solution.nodes[cv]) == 0:
            solution.k -= 1
            solution.nodes.pop(cv)
            solution.unused.append(cv)
            
        solution.nodes[self.c].add(self.v)
        solution.clique[self.v] = self.c
        
        


# In[ ]:


s = p.random_solution()
print(f"random solution:\n{s}")
local_nb = p.local_neighbourhood()
moves = local_nb.moves(s)
for m in moves:
    print(f"Allowed move: {m}")
    
print(f"\napply: {m}")
m.apply_move(s)
print(f"\nSolution: {s}")


# In[ ]:


def best_improvement(solution):
    p = solution.problem
    local_nb = p.local_neighbourhood()
    s = solution.copy_solution()
    
    while True:
        best_move, best_incr = None, math.inf
        for move in local_nb.moves(s):
            incr = move.objective_value_increment(s)
            if incr is not None and incr < best_incr:
                best_move, best_incr = move, incr
        if best_move is None or best_incr >= 0:
            break
        best_move.apply_move(s)
        print(f"best_incr: {best_incr}")
    return s
            


# In[ ]:


s = p.random_solution()
print(f"Random solution: {s}\n")
s = best_improvement(s)
print(f"Best solution found: {s}")


# In[ ]:


f = open("./regnier300-50.txt")
p2 = Problem.from_textio(f)
f.close()

s = p2.random_solution()
print(f"Random solution: {s.objective_value()}\n")
s = best_improvement(s)
print(f"Best solution found: {s.objective_value()}")


# In[ ]:


f = open("./regnier300-50.txt")
p2 = Problem.from_textio(f)
f.close()

s = greedy_algorithm(p2)
print(f"Greedy solution: {s.objective_value()}\n")
s = best_improvement(s)
print(f"Best solution found: {s.objective_value()}")


# In[ ]:




