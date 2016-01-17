import pickle
def save():
	import processbike
	graph = processbike.buildgraph()
	with open("graphbike.pickle", "wb") as outfile:
		pickle.dump(graph, outfile)
def load():
	with open("graphbike.pickle", "rb") as infile:
		return pickle.load(infile)
if __name__ == "__main__":
	save()
