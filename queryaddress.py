import pickleaddress
import picklegraph
import picklestreet
import util
addresses = pickleaddress.load()
gr = picklegraph.load()
streets = picklestreet.load()

def get_dir_helper(dlat, dlon):
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

LEFT = "L"
RIGHT = "R"
def flip(a):
	if a == LEFT:
		return RIGHT
	return LEFT

def getaddress(name):
	"""
	returns: inter, dist, side, longitude, latitude
	"""
	address = addresses.get(name, None)
	if address == None:
		return None, None, None
	inters = streets[address["street"]]
	dist = address["dist"] / 1000 # to kilometers
	side = address["side"]
	alat = address["lat"]
	alon = address["lon"]
	return inters, dist, side, alat, alon

def streetdist(i, edge, dist):
	if i == 0:
		return dist
	return edge["length"] - dist

def address_to_inter(startname, endname):
	"""
	start_inter
	end_inter
	start_dist
	end_dist
	end_side
	"""
	starti, startd, starts, slat, slon = getaddress(startname)
	endi, endd, ends, elat, elon = getaddress(endname)
	if starti == None or endi == None:
		return None, None, None, None, None
	startedge = gr[starti[0]][starti[1]]
	endedge = gr[endi[0]][endi[1]]
	d = None
	for i in range(2):
		for j in range(2):
			si = starti[i]
			ei = endi[j]
			sd = streetdist(i, startedge, startd)
			ed = streetdist(j, endedge, endd)
			es = flip(ends) if j == 1 else ends
			si_latlon = (gr.node[si]["lat"], gr.node[si]["lon"])
			ei_latlon = (gr.node[ei]["lat"], gr.node[ei]["lon"])
			hav = util.hav(si_latlon, ei_latlon)
			# direction from initial address to initial intersection
			si_lon = gr.node[si]['lon']
			si_lat = gr.node[si]['lat']
			start_direction = get_dir_helper(si_lat - slat, si_lon - slon)
			if d == None or hav < d[0]:
				d = (hav, si, ei, sd, ed, es, start_direction)
	return d[1:]

if __name__ == "__main__":
	print(address_to_inter("89 Chestnut St", "655 Bloor St W"))
