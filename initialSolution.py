# Opens an instance of the problem
instance = open("instances/cmb01", "r")

# Reads all of its lines
instanceLines = instance.readlines()

# Grabs its parameters
[numVertices, numEdges, numColors] = map(int, instanceLines[0].split())

weights = list(map(float, instanceLines[1].split()))

edges = []
for line in instanceLines[2:2+numEdges]:
    edgeTuple = tuple(( int(line.split()[0]) , int(line.split()[1]) ))
    edges.append(edgeTuple)

instance.close()

'''
print(numVertices, numEdges, numColors)
print(weights)
print(edges)
'''
