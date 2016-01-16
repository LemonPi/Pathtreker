import haversine

def hav(lonlata, lonlatb):
	"""
	Calculate the Haversine distance in kilometers of two points on Earth
	Arguments:
	lonlata: pair of (lon, lat) in degrees
	lonlatb: pair of (lon, lat) in degrees
	"""
	return haversine.haversine(lonlata[::-1], lonlatb[::-1])