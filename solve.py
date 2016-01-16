import math
import route
import networkx

def solvefile(graph, filename):
	"""
	Load file with pairs of intersections and calculate shortest path between them
	"""
	with open(filename, "r", encoding="utf-8") as infile:
		num = int(infile.readline())
		costs = [0]*num
		for i in range(num):
			source = int(infile.readline())
			dest = int(infile.readline())
			pathcost, _ = route.shortest_path(graph, source, dest)
			costs[i] = pathcost[dest]
	return costs

def testfile(graph, input_name, output_name):
	EPSILON = 0.005 # km
	costs = solvefile(graph, input_name)
	with open(output_name, "r", encoding="utf-8") as infile:
		for i in range(len(costs)):
			theval = float(infile.readline())
			print(costs[i])
			if abs(theval - costs[i]) > EPSILON:
				print("Failed test case", input_name, i, "expected", costs[i], "got", theval)

def dotest(graph):
	testfile(graph, "sample_input.txt", "sample_output.txt")