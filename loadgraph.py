import shapefile
import networkx
import util
import math

# ap_sf = shapefile.Reader("address/ADDRESS_POINT_WGS84")
tcl_sf = shapefile.Reader("centerline/CENTRELINE_WGS84")
intersect_sf = shapefile.Reader("centerline-intersection/CENTRELINE_INTERSECTION_WGS84")

"""Feature codes that are considered in the centreline data"""
tcl_features = set([
    201200, # Major Arterial Road
    201201, # Major Arterial Road Ramp
    201300, # Minor Arterial Road
    201301, # Minor Arterial Road Ramp
    201400, # Collector Road
    201401, # Collector Road Ramp
    201500, # Local Road
    201600, # Other Road
    201601, # Other Ramp
    201700, # Laneways
    201800  # Pending
])

def getcolumnindex(sf, name):
    """
    Get the index of a shapefile's column by name
    """
    for i in range(len(sf.fields)):
        if sf.fields[i][0] == name:
            return (i - 1)
    raise Exception("Column not found: " + name)
tcl_from_column = getcolumnindex(tcl_sf, "FNODE")
tcl_to_column = getcolumnindex(tcl_sf, "TNODE")
tcl_id_column = getcolumnindex(tcl_sf, "GEO_ID")
tcl_fcode_column = getcolumnindex(tcl_sf, "FCODE")

intersect_id_column = getcolumnindex(intersect_sf, "INT_ID")
intersect_lon_column = getcolumnindex(intersect_sf, "LONGITUDE")
intersect_lat_column = getcolumnindex(intersect_sf, "LATITUDE")

def centerline_length(shape):
    """
    Calculate the length of a pyshp line in kilometers using the Haversine formula.
    """
    if shape.shapeType != 3:
        raise Exception("Can't calculate length of non-line shape: " + str(shape.shapeType))
    p = shape.points
    l = 0
    for i in range(len(p) - 1):
        p0 = p[i]
        p1 = p[i + 1]
        l += util.hav((math.radians(p0[0]), math.radians(p1[1])),
                       (math.radians(p1[0]), math.radians(p1[1])))
    return l

def buildgraph():
    """
    Build a networkx graph from centreline and intersection data with weight as length of the street
    Only the centerline types in tcl_features are considered.
    The format of each node is:
     (key): the intersection ID
     lat: Latitude in degrees (WGS84)
     lon: Longitude in degrees (WGS84)
     record: the original record from pyshp
    The format of each edge is:
     length: length of the centerline in km (calculated using Haversine on each of its points)
    """
    G = networkx.Graph()
    for intersect in intersect_sf.iterRecords():
        intersect_id = intersect[intersect_id_column]
        intersect_lon = intersect[intersect_lon_column]
        intersect_lat = intersect[intersect_lat_column]
        G.add_node(intersect_id, lat=intersect_lat, lon=intersect_lon, record=intersect)
    tcl_sf_shapes = tcl_sf.shapes()
    for centerline in tcl_sf.iterRecords():
        cl_index = 0
        cl_type = centerline[tcl_fcode_column]
        if not cl_type in tcl_features:
            cl_index += 1
            continue
        cl_from = centerline[tcl_from_column]
        cl_to = centerline[tcl_to_column]
        cl_length = centerline_length(tcl_sf_shapes[cl_index])
        G.add_edge(cl_from, cl_to, length=cl_length)
        cl_index += 1
    return G
        
def solvefile(filename):
    """
    Load file with pairs of intersections and calculate shortest path between them
    """
    pass

