import queue
import networkx
from math import radians, sin, cos, sqrt, asin
from util import hav


def shortest_path(g, source, dest):
	"""Return single source single destination shortest path using A* search.

	Haversine distance is used as heuristic.

	Arguments:
	g 		-- networkx graph loaded from shapefile
	source 	-- source intersection's index in g
	dest 	-- destination intersection's index in g
	"""

	def heuristic(a,b):	
		"""Return heuristic distance between two nodes in g.

		Haversine distance guranteed to be shorter than actual distance,
		since it's the shortest distance between points on a sphere
		(which the earth approximates).

		Arguments:
		a -- one node index in g
		b -- another node index in g
		"""
		# lat and lon internally stored in degrees, convert and call function
		lona, lonb, lata, latb = map(radians, [g.node[a]['lon'], g.node[b]['lon'], g.node[a]['lat'], g.node[b]['lat']])
		return hav((lona, lata), (lonb, latb))

	# frontier of nodes to explore
	exploring = queue.PriorityQueue()

	# property maps which will be built and returned outside
	# actual cost to node
	cost = {}
	# which immediate node was the shortest path from
	parent = {}

	# queue.PriorityQueue expects put(priority, data) we store node index as data
	exploring.put((0,source))
	parent[source] = None
	cost[source] = 0

	while not exploring.empty():
		u_cost, u = exploring.get()

		if u == dest:
			break

		for v in g[u]:
			new_cost = cost[u] + g[u][v]['length']
			if v not in cost or new_cost < cost[v]:
				# relax edge with new_cost
				cost[v] = new_cost
				parent[v] = u
				heuristic_cost = new_cost + heuristic(u,v)
				# doesn't matter if v's already in exploring queue with higher cost
				# we'll have duplicate nodes, but those won't affect correctness
				# since they'll be explored after the cheaper ones are explored,
				# they won't yield any new shorter paths
				exploring.put((heuristic_cost,v))

	return cost, parent