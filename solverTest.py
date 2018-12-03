# Import PuLP modeler functions
from pulp import *

vertices = [1, 2, 3, 4, 5]
colors = [1, 2, 3]

edges = [(1,2), (1,3), (2,4), (3,5), (4,5)]
weights = [1, 3, 5, 2, 4]


# Create the 'prob' variable to contain the problem data
prob = LpProblem("Most Balanced Graph Coloring",LpMinimize)

x = []
for v in vertices:
    x.append([])
    for c in colors:
        x[v-1].append(LpVariable("x - vertex " + str(v) + " - color " + str(c),0,1,LpInteger))
z = LpVariable("z", 0, None, LpContinuous)

# The objective function is added to 'prob' first
prob += z, "Value of the highest sum of weights in any color"

# The five constraints are entered
for v in vertices:
    prob += lpSum([x[v-1][c-1] for c in colors]) == 1, "Vertex " + str(v-1) + " must only have one color"

for edge in edges:
    for c in colors:
        prob += x[edge[0]-1][c-1] + x[edge[1]-1][c-1] <= 1, "Edge " + str(edge) + " cannot connect 2 vertices of the color" + str(c-1)

for c in colors:
    prob += z >= lpSum([x[v-1][c-1] * weights[v-1] for v in vertices]), "z must be higher than the sum of weights in color " + str(c-1)

# The problem data is written to an .lp file
prob.writeLP("Coloring.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve(GLPK())

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Minimum value for the highest sum of weights in any color = ", value(prob.objective))
