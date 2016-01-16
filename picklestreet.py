import pickle
def save():
	import loadgraph
	streets = {}
	for record in loadgraph.tcl_sf.iterRecords():
		street = (record[loadgraph.tcl_from_column],
			record[loadgraph.tcl_to_column])
		streets[record[loadgraph.tcl_id_column]] = street
	with open("streets.pickle", "wb") as outfile:
		pickle.dump(streets, outfile)

def load():
	with open("streets.pickle", "rb") as infile:
		return pickle.load(infile)

if __name__ == "__main__":
	save()
