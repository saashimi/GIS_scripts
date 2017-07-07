# Name: addr_density.py
# Python 2.7 script

import arcinfo, arcpy
arcpy.CheckOutExtension("Spatial")

#set environment settings
foldername = "C:/Users/kms22/Desktop/py_desktop/address_geocode/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = foldername

# near analysis will update the fc with new columns
fc = foldername + "2016_FT.shp"
in_features = fc
near_features = "I:/Staff/PSRE/PSRE_Planning/--Resources/CPO_GIS/Projects/StudentAddress/2015/SMSU.shp"
arcpy.Near_analysis(in_features, near_features)

# insert new field 
field_name = "DIST_MI"
field_type = "FLOAT"
arcpy.AddField_management(in_features, field_name, field_type)

# convert feet to miles
fields = ["NEAR_DIST", "DIST_MI"]
FT_IN_MI=5280.
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        row[1] = row[0]/FT_IN_MI
        cursor.updateRow(row)

# generate kernel density map
#SIXTEENTH_MI=330
population_field = "NONE"
cellSize = 330 # 1/16 of a mile
area_unit_scale_factor = "SQUARE_MILES"
out_cell_values = "DENSITIES"
method="GEODESIC"
searchRadius = 168960 # 32 Miles

outKernelDensity = arcpy.sa.KernelDensity(in_features, population_field, cellSize, searchRadius, area_unit_scale_factor, out_cell_values, method)
outKernelDensity.save("kdmap")

arcpy.CheckInExtension("Spatial")
# import 5, 10, 15, 20-mile symbology

