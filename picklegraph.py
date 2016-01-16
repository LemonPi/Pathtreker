import pickle
def dump():
	import loadgraph
	graph = loadgraph.buildgraph()
	print("done building")
	with open("graph.pickle", "wb") as f:
		pickle.dump(graph, f)

def load():
	with open("graph.pickle", "rb") as f:
		return pickle.load(f)

if __name__ == "__main__":
	dump()
