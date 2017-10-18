"""
This script assumes that the following fields have been added to your shapefile:
START_Y, START_X - Start coordinate of each polyline
END_Y, END_X - End coordinate of each polyline
LEN_FT - The length in feet of each polyline 
"""
import arcpy
import numpy
import timeit

# Set environment
mxd = arcpy.mapping.MapDocument("CURRENT")
#kate = "V:/allStreetsNetwork/all-modes-network/shp/2015_Kate_101117_link.shp"
kate = "V:/allStreetsNetwork/all-modes-network/shp/test_kate.shp"
bike = "V:/allStreetsNetwork/all-modes-network/shp/test_bike_sm.shp"


def dist_eucl(val_x, val_y):
    """
    calculates the euclydian distance between two points using numpy library.
    """
    return numpy.linalg.norm(val_x - val_y)


# Loop through feature classes
fields = ["NO", "START_Y", "START_X", "END_Y", "END_X", "LEN_FT"]

tolerance_ft = 25.0

start_time = timeit.default_timer()
hits = 0
NOs = []

with arcpy.da.SearchCursor(bike, fields) as bike_rows:
    for bike_row in bike_rows:    
        with arcpy.da.SearchCursor(kate, fields) as kate_rows:
            for kate_row in kate_rows:           
                kate_start = numpy.array((kate_row[2], kate_row[1])) 
                bike_start = numpy.array((bike_row[2], bike_row[1])) 
                kate_end = numpy.array((kate_row[4], kate_row[3])) 
                bike_end = numpy.array((bike_row[4], bike_row[3]))
                kate_len = kate_row[5]
                bike_len = bike_row[5] 

                #print dist_eucl(kate_start, bike_start), dist_eucl(kate_end, bike_end)
                
                if ((dist_eucl(kate_start, bike_start) <= tolerance_ft or
                    dist_eucl(kate_end, bike_end) <= tolerance_ft) and 
                    abs(bike_len - kate_len) <= tolerance_ft):
                    hits += 1
                    NOs.append(kate_row[0])
        
                else:
                    continue

try:
    exp = '"NO" IN (' + ','.join(map(str, NOs)) + ')'
    arcpy.SelectLayerByAttribute_management("test_kate", "NEW_SELECTION", exp)

except:
    print 'No hits or other error.'

    
elapsed = timeit.default_timer() - start_time
print str(hits) + " hits"
print str(elapsed) + " seconds"


