from math import sin, cos, asin, sqrt

def hav(lonlata, lonlatb):
	# ported from latlontools
	# assume latitude and longitudes are in radians
	lona = lonlata[0]
	lata = lonlata[1]

	lonb = lonlatb[0]
	latb = lonlatb[1]
	
	diff_lat = lata - latb
	diff_lon = lona - lonb

	a = sin(diff_lat/2)**2 + cos(lona) * cos(latb) * sin(diff_lon/2)**2
	c = 2 * asin(sqrt(a)) 
	r = 6371 # radius of earth in km
	return c * r