"""
This script assumes that the following fields have been added to your shapefile:
START_Y, START_X - Start coordinate of each polyline
END_Y, END_X - End coordinate of each polyline
LEN_FT - The length in feet of each polyline 
"""

import timeit

# Set environment
mxd = arcpy.mapping.MapDocument("CURRENT")
kate = "V:/allStreetsNetwork/allModes/shp/2015_Kate_101117_link.shp"
bike = "V:/allStreetsNetwork/allModes/shp/test_bike.shp"
fields = ["NO", "START_Y", "START_X", "END_Y", "END_X", "LEN_FT"]

# Loop through feature classes
kate_rows = arcpy.SearchCursor(kate, fields)
bike_rows = arcpy.SearchCursor(bike, fields)
tolerance_ft = 15.0

start_time = timeit.default_timer()
hits = 0
NOs = []
for bike_row in bike_rows:    
    for kate_row in kate_rows:
        if (abs(kate_row.getValue("START_Y") - bike_row.getValue("START_Y")) <= tolerance_ft or
            abs(kate_row.getValue("START_X") - bike_row.getValue("START_X")) <= tolerance_ft or
            abs(kate_row.getValue("END_Y") - bike_row.getValue("END_Y")) <= tolerance_ft or
            abs(kate_row.getValue("END_X") - bike_row.getValue("END_X")) <= tolerance_ft):
            hits += 1
            NOs.append(kate_row.getValue("NO"))
        
        else:
            continue

exp = '"NO" IN (' + ','.join(map(str, NOs)) + ')'
arcpy.SelectLayerByAttribute_management("2015_Kate_101117_link", "NEW_SELECTION", exp)

    
elapsed = timeit.default_timer() - start_time
print str(hits) + " hits"
print str(elapsed/60.0) + " minutes"


