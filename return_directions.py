import route
import math
import picklegraph
from flask import Flask, request, jsonify
# backend to webapp that returns direction JSON object as defined in doc/backend_api
app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)

# load serialized graph quickly
centerline_graph = picklegraph.load()

# intersection record indices
name_index = 2

def get_dir(start_inter, end_inter):
	"""Return direction when given adjacent starting and ending intersections."""
	# compare the difference in longitude and latitude
	start_lon = centerline_graph.node[start_inter]['lon']
	start_lat = centerline_graph.node[start_inter]['lat']
	end_lon = centerline_graph.node[end_inter]['lon']
	end_lat = centerline_graph.node[end_inter]['lat']
	dlat = end_lat - start_lat
	dlon = end_lon - start_lon
	if abs(dlat) > abs(dlon):
		# more difference along latitude, either N or S
		if dlat > 0:
			return "North"
		else:
			return "South"
	else:
		if dlon > 0:
			return "East"
		else:
			return "West"

turn = {
	"North": {
		"West":"left",
		"East":"right"
	},
	"South": {
		"West":"right",
		"East":"left"
	},
	"East": {
		"North":"left",
		"South":"right"
	},
	"West": {
		"North":"right",
		"South":"left"	
	}
}


@app.route('/direction', methods=['GET'])
def get_direction():
	"""
	Arguments from request:
	start -- starting address point 
	end	  -- ending address point
	"""
	start = request.args.get('start')
	end = request.args.get('end')

	# intersection indices, and distances from address to those intersections
	start_inter, end_inter, start_dist, end_dist, end_side = address_to_inter(start, end)

	instructions = {"error":None, "length":-1, "path":[]}

	dists, parent = route.shortest_path(centerline_graph, start_inter, end_inter)
	print("successfully found shortest path")
	# based on parent, return certain instructions

	node = end
	path = []
	# start with last street
	prev_street = centerline_graph[parent[node]][node]["street"]
	while parent[node]: 
		print("{}<-{}".format(node, parent[node]))
		to_inter = centerline_graph.node[node]
		from_inter = centerline_graph.node[parent[node]]
		edge = centerline_graph[parent[node]][node]

		cur_street = edge["street"]

		# debugging
		instructions["path"].append(str(from_inter))
		instructions["path"].append(str(to_inter))
		instructions["path"].append(str(edge))

		# create instruction
		instruct = {}
		# arrived at end, give 2 instructions
		# additional one from final intersection to ending address
		if node == end_inter:
			# going from final intersection to ending address
			instruct["action"] = "arrive"
			instruct["side"] = end_side
			instruct["distance"] = end_dist
			path.append(instruct)
			# create new one for 2nd instruction
			instruct = {}

		# turn if street changes, else collect into the same along
		if cur_street != prev_street:
			instruct["action"] = "turn"
			prev_street = cur_street
			# compare last street's direction and this street's direction
			from_dir = get_dir(from_inter, to_inter)
			# direction further down the path (previously encountered)
			to_dir = path[-1]["direction"]

			instruct["direction"] = turn[from_dir][to_dir]

		# not turning, heading along straight
		else:
			instruct["action"] = "along"
			if path[-1]["action"] == "turn":
				# just turned, need to create new instruction
				cur_dir = get_dir(from_inter, to_inter)
				instruct["direction"] = get_dir(from_inter, to_inter)
				instruct["from"] = {
					"name":from_inter["record"][name_index],
					"lon":from_inter["lon"],
					"lat":from_inter["lat"]
				}
				instruct["to"] = {
					"name":from_inter["record"][name_index],
					"lon":from_inter["lon"],
					"lat":from_inter["lat"]
				}
				instruct["distance"] = edge["length"]
				path.append(instruct)

			else:
				# already along the same direction, just add to distance and update instruction's from intersection
				instruct = path[-1]
				instruct["from"] = {
					"name":from_inter["record"][name_index],
					"lon":from_inter["lon"],
					"lat":from_inter["lat"]
				}
				instruct["distance"] += edge["length"]				


		# arrived at start, give 2 instructions
		# additional one from initial address to initial intersection
		if parent[node] == start_inter:
			# going from initial address to initial intersection
			instruct["action"] = "along"
			instruct["distance"] = start_dist
			# from address
			instruct["from"] = {
				"name":from_inter["record"][name_index],
				"lon":from_inter["lon"],
				"lat":from_inter["lat"]
			}
			# first intersection
			instruct["to"] = {
				"name":from_inter["record"][name_index],
				"lon":from_inter["lon"],
				"lat":from_inter["lat"]
			}


		# go on to previous part of track
		node = parent[node]

	return jsonify(instructions)
	



if __name__ == '__main__':
    app.run()