# Import PuLP modeler functions
from pulp import *
import time

vertices = 5
colors = 3

edges = [(1,2), (1,3), (2,4), (3,5), (4,5)]
weights = [1.7, 3.2222, 5.8931, 2.0102, 4.5]

t0 = time.time()


# Create the 'prob' variable to contain the problem data
prob = LpProblem("Most Balanced Graph Coloring",LpMinimize)

x = []
for v in range(0, vertices):
    x.append([])
    for c in range(0, colors):
        x[v].append(LpVariable("v" + str(v+1) + "c" + str(c+1),0,1,LpInteger))
z = LpVariable("z", 0, None, LpContinuous)

# The objective function is added to 'prob' first
prob += z, "Value of the highest sum of weights in any color"

# The five constraints are entered
for v in range(0, vertices):
    prob += lpSum([x[v][c] for c in range(0, colors)]) == 1, "Vertex " + str(v+1) + " must only have one color"

for edge in edges:
    for c in range(0, colors):
        prob += x[edge[0]-1][c] + x[edge[1]-1][c] <= 1, "Edge " + str(edge) + " cannot connect 2 vertices of the color " + str(c+1)

for c in range(0, colors):
    prob += z >= lpSum([x[v][c] * weights[v] for v in range(0, vertices)]), "z must be higher than the sum of weights in color " + str(c+1)

# The problem is solved using PuLP's choice of Solver
prob.solve(GLPK())

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

colorSets = [] # A list of all color sets, each represented as a list of the vertices painted with that respective color
for i in range(0, colors):
    colorSets.append([])
setWeights = [0] * colors # List that will contain the weight of each color

# Change the variables to a readable format
for v in prob.variables():
    if v.name != "z":
        if v.varValue == 1:
            vertexColor = int(v.name.split('c')[1]) - 1
            vertexNumber = int(v.name.split('c')[0][1:])
            colorSets[vertexColor].append(vertexNumber)
            setWeights[vertexColor] += weights[vertexNumber-1]

# Print each color set, with its vertices and weight
for i in range(0, colors):
    print("Cor " + str(i + 1) + ", peso = " + str(setWeights[i]))
    print(colorSets[i])

# The optimised objective function value is printed to the screen
print("Valor da solucao: ", value(prob.objective))

t1 = time.time()

print(str(round(t1-t0, 2)))
