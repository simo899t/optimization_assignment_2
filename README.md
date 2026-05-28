# Optimization Assignment 2

---

## Case 1 — Continuous Optimization

Gradient descent and Newton's method with line search on a simplex problem .

```bash
cd src/case1
uv run python main.py
```

---

## Case 2 — Team Formation

Assigns students via the `roar_net_api` framework.

```bash
cd src/case2
uv run python -m testing
```

### Structure

```
model/
  Problem.py           # Problem definition and parser
  Solution.py          # Solution representation
  AddNeighbourhood.py  # Construction neighbourhood
  SwapNeighbourhood.py # Local search neighbourhood
  SA.py                # Simulated annealing
```
