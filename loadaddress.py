import loadgraph
import shapefile

address_sf = shapefile.Reader("address/ADDRESS_POINT_WGS84")

address_index = loadgraph.getcolumnindex(address_sf, "ADDRESS")
lfname_index = loadgraph.getcolumnindex(address_sf, "LFNAME")
arc_side_index = loadgraph.getcolumnindex(address_sf, "ARC_SIDE")
distance_index = loadgraph.getcolumnindex(address_sf, "DISTANCE")
lon_index = loadgraph.getcolumnindex(address_sf, "LONGITUDE")
lat_index = loadgraph.getcolumnindex(address_sf, "LATITUDE")

link_index = loadgraph.getcolumnindex(address_sf, "LINK")

def buildaddress():
	addresses = {}
	for record in address_sf.iterRecords():
		address = record[address_index]
		lfname = record[lfname_index]
		arc_side = record[arc_side_index]
		distance = record[distance_index]
		link = record[link_index]
		a = {
			"name": address + " " + lfname,
			"street": link,
			"side": arc_side,
			"dist": distance,
			"lon": record[lon_index],
			"lat": record[lat_index]
		}
		addresses[a["name"]] = a
	return addresses
