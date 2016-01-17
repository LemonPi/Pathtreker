import picklegraph
import shapefile
import loadgraph
bi_sh = shapefile.Reader("bikeways/CENTRELINE_BIKEWAY_OD_WGS84")
fnode_index = loadgraph.getcolumnindex(bi_sh, "FNODE")
tnode_index = loadgraph.getcolumnindex(bi_sh, "TNODE")
cp_type_index = loadgraph.getcolumnindex(bi_sh, "CP_TYPE")
BIKE_FRIENDLY_SCALE_FACTOR = 0.5
def buildgraph():
	graph = picklegraph.load()
	i = 0
	for record in bi_sh.iterRecords():
		fnode = record[fnode_index]
		tnode = record[tnode_index]
		cp_type = record[cp_type_index]
		if cp_type == None or len(cp_type) == 0 or cp_type[0] == 0x20:
			continue
		if fnode in graph and tnode in graph[fnode]:
			i += 1
			graph[fnode][tnode]["length"] *= BIKE_FRIENDLY_SCALE_FACTOR
	print("changed", i, "lengths")
	return graph
		
