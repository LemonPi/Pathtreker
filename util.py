from math import sin, cos, asin, sqrt

def hav(lona, lonb, lata, latb):
	# ported from latlontools
	# assume latitude and longitudes are in radians
	diff_lat = lata - latb
	diff_lon = lona - lonb

	a = sin(diff_lat/2)**2 + cos(lona) * cos(latb) * sin(diff_lon/2)**2
	c = 2 * asin(sqrt(a)) 
	r = 6371 # radius of earth in km
	return c * r