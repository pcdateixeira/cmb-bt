import operator
import os.path
import time
import sys
from pulp import *

#
# Gets the highest degree of a vertex in the current graph
#

def getMaxDegree(degrees):
    maxDegree = 0
    for i in range(0, numVertices):
        if degrees[i] > maxDegree:
            maxDegree = degrees[i]
    return maxDegree

#
# Gets the value of a solution
#

def getSolutionValue(solution, numColors, weights):
    solWeights = [0] * numColors
    for i in range(0, numColors):
        for vertex in solution[i]:
            solWeights[i] += weights[vertex]
        solWeights[i] = round(solWeights[i], 2)
    return max(solWeights)

#
# Reads the information needed from the instance file
#

def readInstance():
    # Opens an instance of the problem
    while True:
        try:
            fileName = input("Digite o nome do arquivo da instância a ser analisada: ")
            instance = open("instances/" + fileName, "r")
            break
        except FileNotFoundError:
            print("Arquivo não existente ou não encontrado no diretório atual, tente de novo.")

    # Reads all of its lines
    instanceLines = instance.readlines()

    # Grabs its parameters
    [numVertices, numEdges, numColors] = map(int, instanceLines[0].split())

    weights = list(map(float, instanceLines[1].split()))

    degrees = {} # Dictionary that will store the degree of each vertex, to be used to find an initial solution
    for i in range(0, numVertices):
        degrees[i] = 0
    edges = []
    for line in instanceLines[2:2+numEdges]:
        edgeTuple = tuple(( int(line.split()[0]) , int(line.split()[1]) ))
        edges.append(edgeTuple)

        degrees[int(line.split()[0])] += 1
        degrees[int(line.split()[1])] += 1

    instance.close()

    return (fileName, numVertices, numEdges, numColors, weights, edges, degrees)

#
# Reads the initial solution from the previously created file
#

def readInitialSolution(fileName, numColors):
    file = open("solutions/initSol-" + fileName, "r")

    # Reads all of its lines
    fileLines = file.readlines()

    solution = [] # A list of all color sets, each represented as a list of the vertices painted with that respective color
    for i in range(0, numColors):
        solution.append([])

    i = 0
    currentColor = 0
    for line in fileLines:
        if i % 2 != 0 and currentColor < numColors: # In a solution file, every other line contains the vertices of a color
            solution[currentColor] = eval(line)
            currentColor += 1
        i += 1

    return solution

#
# Uses the Welsh-Powell algorithm to find an initial solution with at most d(g) + 1 colors
#

def welshPowell(degrees, edges, numColors):
    solution = [] # A list of all color sets, each represented as a list of the vertices painted with that respective color
    for i in range(0, numColors):
        solution.append([])

    uncoloredVertices = [] # List with possible vertices not colored by Welsh-Powell

    for color in range(0, numColors):
        #print("Starting to add verticed to the color set " + str(color))
        sortedVertByDegree = iter(sorted(degrees.items(), key=operator.itemgetter(1), reverse=True)) # Creates an iterator that goes through the vertices in descending order of their degrees
        cantPaint = 0 # Variable that will determine if the current vertex can be painted or not

        while cantPaint != -1:
            try:
                currentVertex = next(sortedVertByDegree)
            except StopIteration as e:
                break
            cantPaint = 0
            for i in range(0, color+1):
                if currentVertex[0] in solution[i]: # If the vertex was already painted,
                    cantPaint = 1
            if cantPaint == 0:
                solution[color].append(currentVertex[0]) # Paints the first non-colored vertex with the first available color
                #print("Vertex " + str(currentVertex[0]) + " in the color set " + str(color))
                cantPaint = -1

        for currentVertex in sortedVertByDegree:
            cantPaint = 0
            # Checks if the current vertex isn't adjacent to any other vertex painted with the current color
            for edge in edges:
                if edge[0] == currentVertex[0] or edge[1] == currentVertex[0]: # If an edge is associated with the vertex,
                    for coloredVertex in solution[color]:
                        if edge == (currentVertex[0], coloredVertex) or edge == (coloredVertex, currentVertex[0]): # and that edge is also associated with a vertex with the current color,
                            cantPaint = 1

                            if color == (numColors - 1): # Checks for vertices that couldn't be colored by Welsh-Powell
                                cantPaint = -1
                                for i in range(0, color+1):
                                    if currentVertex[0] in solution[i]:
                                        cantPaint = 1
                                if cantPaint == -1 and currentVertex[0] not in uncoloredVertices:
                                    uncoloredVertices.append(currentVertex[0])
                                    cantPaint = 1
            if cantPaint == 0:
                #print("Vertex " + str(currentVertex[0]) + " ready to be added to the current color set")
                for i in range(0, color+1):
                    if currentVertex[0] in solution[i]: # If the vertex was already painted,
                        cantPaint = 1
                if cantPaint == 0:
                    solution[color].append(currentVertex[0])
                    #print("The current color set has " + str(len(colorSets[color])) + " vertices")

    return (solution, uncoloredVertices)

#
# Finds an initial solution with k colors
#

def initialSolution(degrees, edges, numColors, weights, fileName):
    ti = time.time()
    (solution, uncoloredVertices) = welshPowell(degrees, edges, numColors)

    #iteration = 0
    maxDegree = getMaxDegree(degrees)
    origDegrees = degrees

    while uncoloredVertices: # If there are any uncolored vertices after one iteration of Welsh-Powell,
        #iteration += 1
        #print(iteration)
        for uncoloredVertex in uncoloredVertices:
                if degrees[uncoloredVertex] < maxDegree:
                    degrees[uncoloredVertex] += 1 # Artifically increases those vertices' degrees, so they get picked earlier in a future iteration
                #else:
                    #degrees[uncoloredVertex] = origDegrees[uncoloredVertex]

        print(uncoloredVertices)
        prevUncolored = uncoloredVertices

        (solution, uncoloredVertices) = welshPowell(degrees, edges, numColors)

        #if len(uncoloredVertices) > len(prevUncolored):
            #uncoloredVertices = prevUncolored

        if uncoloredVertices == prevUncolored:
            #degrees[random.randint(0, numVertices)] -= 1
            degrees = origDegrees


    tf = time.time()
    timer = tf - ti

    # Writes the solution into a file

    solWeights = [0] * numColors
    for i in range(0, numColors):
        for vertex in solution[i]:
            solWeights[i] += weights[vertex]
        solWeights[i] = round(solWeights[i], 2)

            #print("Cor " + str(i + 1) + ": " + str(len(colorSets[i])) + " vértices, peso = " + str(setWeights[i]))

    initialSolution = open("solutions/initSol-" + fileName, "w")
    for i in range(0, numColors):
        initialSolution.write("Cor " + str(i + 1) + ", peso = " + str(solWeights[i]) + "\n")
        initialSolution.write(str(solution[i]) + "\n")
    initialSolution.write("Valor da solucao: " + str(max(solWeights)) + "\n")
    if timer < 60:
        initialSolution.write("Tempo percorrido: " + str(round(timer, 2)) + " segundos\n")
    elif timer < 3600:
        initialSolution.write("Tempo percorrido: " + str(round( (timer/60), 2)) + " minutos\n")
    else:
        initialSolution.write("Tempo percorrido: " + str(round( (timer/3600), 2)) + " horas\n")

    initialSolution.close()

    return solution

#
# Uses GLPK to solve the formulated problem
#

def solverSolution(fileName, numVertices, numColors, edges, weights):

    ti = time.time()

    # Create the 'prob' variable to contain the problem data
    prob = LpProblem("Most Balanced Graph Coloring",LpMinimize)

    # Create the problem's variables
    x = []
    for v in range(0, numVertices):
        x.append([])
        for c in range(0, numColors):
            x[v].append(LpVariable("v" + str(v+1) + "c" + str(c+1),0,1,LpInteger))
    z = LpVariable("z", 0, None, LpContinuous)

    # The objective function is added to 'prob' first
    prob += z, "Value of the highest sum of weights in any color"

    # The three series of constraints are entered
    for v in range(0, numVertices):
        prob += lpSum([x[v][c] for c in range(0, numColors)]) == 1, "Vertex " + str(v+1) + " must only have one color"

    for edge in edges:
        for c in range(0, numColors):
            prob += x[edge[0]-1][c] + x[edge[1]-1][c] <= 1, "Edge " + str(edge) + " cannot connect 2 vertices of the color " + str(c+1)

    for c in range(0, numColors):
        prob += z >= lpSum([x[v][c] * weights[v] for v in range(0, numVertices)]), "z must be higher than the sum of weights in color " + str(c+1)

    # The problem is solved using GLPK
    prob.solve(GLPK(options=["--tmlim", str(60*60*4)])) # Set a time limit for 4 hours

    tf = time.time()
    timer = tf - ti

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    colorSets = [] # A list of all color sets, each represented as a list of the vertices painted with that respective color
    for i in range(0, numColors):
        colorSets.append([])
    setWeights = [0] * numColors # List that will contain the weight of each color

    # Change the variables to a readable format
    for v in prob.variables():
        if v.name != "z":
            if v.varValue == 1:
                vertexColor = int(v.name.split('c')[1]) - 1
                vertexNumber = int(v.name.split('c')[0][1:])
                colorSets[vertexColor].append(vertexNumber)
                setWeights[vertexColor] += weights[vertexNumber-1]

    # Writes the solution to a file
    solverSolution = open("solutions/solverSol-" + fileName, "w")
    for i in range(0, numColors):
        setWeights[i] = round(setWeights[i], 2)
        solverSolution.write("Cor " + str(i + 1) + ", peso = " + str(setWeights[i]) + "\n")
        solverSolution.write(str(colorSets[i]) + "\n")
    solverSolution.write("Valor da solucao: " + str(value(prob.objective)) + "\n")
    if timer < 60:
        solverSolution.write("Tempo percorrido: " + str(round(timer, 2)) + " segundos\n")
    elif timer < 3600:
        solverSolution.write("Tempo percorrido: " + str(round( (timer/60), 2)) + " minutos\n")
    else:
        solverSolution.write("Tempo percorrido: " + str(round( (timer/3600), 2)) + " horas\n")
    solverSolution.close()

# Beginning of the script

try:
    outputFile = sys.argv[1]
except IndexError:
    print("\nParâmetros insuficientes. Formato esperado:\n")
    print("python cmb-bt.py <arquivo>")
    print("    * <arquivo>: nome do arquivo no qual guardar a solução final.")
    sys.exit(1)

(fileName, numVertices, numEdges, numColors, weights, edges, degrees) = readInstance()

if not os.path.isfile("solutions/initSol-" + fileName):
    currentSol = initialSolution(degrees, edges, numColors, weights, fileName)
else:
    currentSol = readInitialSolution(fileName, numColors)

bestSolValue = getSolutionValue(currentSol, numColors, weights)
bestSol = currentSol
tabuList = []

'''while criteria:
    currentSol = bestNeighbor(currentSol)
    if getSolutionValue(currentSol) < bestSolValue:
        bestSolValue = getSolutionValue(currentSol)
        bestSol = currentSol
    tabuList.append(movement)'''

solverSolution(fileName, numVertices, numColors, edges, weights)
