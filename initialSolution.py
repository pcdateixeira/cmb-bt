import operator
import random

#
# Grabs the information needed from the instance
#

def getInstance():
    # Opens an instance of the problem
    fileName = input("Digite o nome do arquivo da instância a ser analisada: ")
    instance = open("instances/" + fileName, "r")

    # Reads all of its lines
    instanceLines = instance.readlines()

    # Grabs its parameters
    [numVertices, numEdges, numColors] = map(int, instanceLines[0].split())

    weights = list(map(float, instanceLines[1].split()))

    degrees = {} # Dictionary that will store the degree of each vertex, to be used to find an initial solution
    for i in range(0, numVertices):
        degrees[i] = 0
    if int(fileName[3:]) > 6:
        numColors += 1
    edges = []
    for line in instanceLines[2:2+numEdges]:
        edgeTuple = tuple(( int(line.split()[0]) , int(line.split()[1]) ))
        edges.append(edgeTuple)

        degrees[int(line.split()[0])] += 1
        degrees[int(line.split()[1])] += 1

    instance.close()

    return (fileName, numVertices, numEdges, numColors, weights, edges, degrees)

#
# Uses the Welsh-Powell algorithm to find an initial solution with at most d(g) + 1 colors
#

def welshPowell(degrees, edges, numColors):
    colorSets = [] # A list of all color sets, each represented as a list of the vertices painted with that respective color
    for i in range(0, numColors):
        colorSets.append([])

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
                if currentVertex[0] in colorSets[i]: # If the vertex was already painted,
                    cantPaint = 1
            if cantPaint == 0:
                colorSets[color].append(currentVertex[0]) # Paints the first non-colored vertex with the first available color
                #print("Vertex " + str(currentVertex[0]) + " in the color set " + str(color))
                cantPaint = -1

        for currentVertex in sortedVertByDegree:
            cantPaint = 0
            # Checks if the current vertex isn't adjacent to any other vertex painted with the current color
            for edge in edges:
                if edge[0] == currentVertex[0] or edge[1] == currentVertex[0]: # If an edge is associated with the vertex,
                    for coloredVertex in colorSets[color]:
                        if edge == (currentVertex[0], coloredVertex) or edge == (coloredVertex, currentVertex[0]): # and that edge is also associated with a vertex with the current color,
                            cantPaint = 1

                            if color == (numColors - 1): # Checks for vertices that couldn't be colored by Welsh-Powell
                                cantPaint = -1
                                for i in range(0, color+1):
                                    if currentVertex[0] in colorSets[i]:
                                        cantPaint = 1
                                if cantPaint == -1 and currentVertex[0] not in uncoloredVertices:
                                    uncoloredVertices.append(currentVertex[0])
                                    cantPaint = 1
            if cantPaint == 0:
                #print("Vertex " + str(currentVertex[0]) + " ready to be added to the current color set")
                for i in range(0, color+1):
                    if currentVertex[0] in colorSets[i]: # If the vertex was already painted,
                        cantPaint = 1
                if cantPaint == 0:
                    colorSets[color].append(currentVertex[0])
                    #print("The current color set has " + str(len(colorSets[color])) + " vertices")

    return (colorSets, uncoloredVertices)

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
# Finds an initial solution with k colors
#

def findInitialSolution(degrees, edges, numColors):
    (colorSets, uncoloredVertices) = welshPowell(degrees, edges, numColors)

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

        (colorSets, uncoloredVertices) = welshPowell(degrees, edges, numColors)

        #if len(uncoloredVertices) > len(prevUncolored):
            #uncoloredVertices = prevUncolored

        if uncoloredVertices == prevUncolored:
            #degrees[random.randint(0, numVertices)] -= 1
            degrees = origDegrees

    return colorSets

#
# Saves the initial solution in a file
#

def saveInitialSolution(fileName, numColors, colorSets, weights):
    if int(fileName[3:]) > 6:
        numColors -= 1
        colorSets[numColors - 1] += colorSets[numColors]
    setWeights = [0] * numColors
    for i in range(0, numColors):
        for vertex in colorSets[i]:
            setWeights[i] += weights[vertex]
        setWeights[i] = round(setWeights[i], 2)

        print("Cor " + str(i + 1) + ": " + str(len(colorSets[i])) + " vértices, peso = " + str(setWeights[i]))

    initialSolution = open("solutions/sol-" + fileName, "w")
    for i in range(0, numColors):
        initialSolution.write("Cor " + str(i + 1) + ", peso = " + str(setWeights[i]) + "\n")
        initialSolution.write(str(colorSets[i]) + "\n")
    initialSolution.close()


# Beginning of the script

(fileName, numVertices, numEdges, numColors, weights, edges, degrees) = getInstance()

colorSets = findInitialSolution(degrees, edges, numColors)

saveInitialSolution(fileName, numColors, colorSets, weights)

# Tabu search



'''
print(numVertices, numEdges, numColors)
print(weights)
print(edges)
print(vertByDegree)
'''
