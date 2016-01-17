import route
import math
import picklegraph
import picklegraph_bike
from queryaddress import address_to_inter, get_dir_helper
from flask import Flask, request, jsonify
# backend to webapp that returns direction JSON object as defined in doc/backend_api
app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)

# load serialized graph quickly (takes less than a second from previous time of 37 seconds)
centerline_graph = picklegraph.load()
bikelane_graph = picklegraph_bike.load()

# intersection record indices
name_index = 2

def get_dir(g, start_inter, end_inter):
	"""Return direction of path segment when given adjacent starting and ending intersections."""
	# compare the difference in longitude and latitude
	start_lon = g.node[start_inter]['lon']
	start_lat = g.node[start_inter]['lat']
	end_lon = g.node[end_inter]['lon']
	end_lat = g.node[end_inter]['lat']
	dlat = end_lat - start_lat
	dlon = end_lon - start_lon
	return get_dir_helper(dlat,dlon)


# used as turn[in_dir][out_dir] to see which direction to turn
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
	"""Return JSON instruction object when given starting and ending address.

	Instruction object is documented in doc/backend_api

	Arguments from request:
	start -- starting address name
	end	  -- ending address name
	bike_mode -- true or false, decides which graph to use
	"""
	start = request.args.get('start')
	end = request.args.get('end')
	bike_mode = request.args.get('bike_mode')
	if bike_mode:
		print("using bike mode")

	# intersection indices, and distances from address to those intersections
	start_inter, end_inter, start_dist, end_dist, end_side, start_dir = address_to_inter(start, end)

	instructions = {"error":None, "length":-1, "path":[]}

	working_graph = bikelane_graph if bike_mode == "true" else centerline_graph

	dists, parent = route.shortest_path(working_graph, start_inter, end_inter)
	print("successfully found shortest path")
	# based on parent, return certain instructions

	node = end_inter
	path = []
	# start with last street
	prev_street = working_graph[parent[node]][node]["street"]

	# going from final intersection to ending address
	instruct = {}
	instruct["action"] = "arrive"
	instruct["side"] = end_side
	instruct["distance"] = end_dist
	print(start_dir)
	instruct["direction"] = start_dir
	path.append(instruct)

	# do the reste of the travelling
	while parent[node]: 
		# we are going from parent[node] -> node
		print("{}<-{}".format(node, parent[node]))
		to_inter = working_graph.node[node]
		from_inter = working_graph.node[parent[node]]
		edge = working_graph[parent[node]][node]

		cur_street = edge["street"]

		# debugging
		# instructions["path"].append(str(from_inter))
		# instructions["path"].append(str(to_inter))
		# instructions["path"].append(str(edge))


		# turn if street changes
		if cur_street != prev_street:
			# update to new turned to street
			prev_street = cur_street
			# need to create new instruction
			instruct = {}

			instruct["action"] = "turn"
			# compare last street's direction and this street's direction
			from_dir = get_dir(working_graph, parent[node], node)
			# direction further down the path (previously encountered)
			to_dir = path[-1]["direction"]

			try:
				instruct["direction"] = turn[from_dir][to_dir]
			except KeyError:
				print("from {} to {}".format(from_dir, to_dir))
				if (from_dir == to_dir):
					instruct["direction"] = "Toward"
				else:
					instruct["direction"] = "Around"

			instruct["from"] = {
				"name":from_inter["record"][name_index],
				"lon":from_inter["lon"],
				"lat":from_inter["lat"]
			}
			instruct["to"] = {
				"name":to_inter["record"][name_index],
				"lon":to_inter["lon"],
				"lat":to_inter["lat"]
			}
			path.append(instruct)
		
		if path[-1]["action"] == "turn":
			# just turned, need to create new instruction
			instruct = {}
			instruct["action"] = "along"

			instruct["direction"] = get_dir(working_graph, parent[node], node)
			instruct["from"] = {
				"name":from_inter["record"][name_index],
				"lon":from_inter["lon"],
				"lat":from_inter["lat"]
			}
			instruct["to"] = {
				"name":to_inter["record"][name_index],
				"lon":to_inter["lon"],
				"lat":to_inter["lat"]
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

		# go on to previous part of track
		node = parent[node]

	# go from initial address to initial intersection
	instruct = {}
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

	instructions["path"] = list(reversed(path))
	# from initial address to initial intersection to final intersection to final address
	instructions["length"] = start_dist + dists[end_inter] + end_dist

	return jsonify(instructions)

@app.route("/")
def root():
	return open("static/index.html").read()
	

if __name__ == '__main__':
    app.run()
