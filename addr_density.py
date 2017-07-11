# Name: addr_density.py
# Python 2.7 script
# Generates a Kernel density map of student addresses. Requires Spatial Analyst 
# license.

import arcinfo, arcpy
arcpy.CheckOutExtension("Spatial")

#set environment settings
foldername = "C:/Users/kms22/Desktop/compy_desktop/data_holding/address_geocode/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = foldername
fileList = arcpy.ListFeatureClasses()

for featureClass in fileList:

    # near analysis will update the fc with new columns
    print "Now processing " + featureClass + "."
    fc = featureClass
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
    population_field = "NONE"
    cellSize = 330 #1/16 of a mile
    area_unit_scale_factor = "SQUARE_MILES"
    out_cell_values = "DENSITIES"
    method="PLANAR"
    searchRadius = 5280 #1 Mile
    saveName = "kd" + featureClass[:-4]

    outKernelDensity = arcpy.sa.KernelDensity(in_features, population_field, cellSize, searchRadius, area_unit_scale_factor, out_cell_values, method)
    outKernelDensity.save(saveName)

# check in Spatial Analyst license
arcpy.CheckInExtension("Spatial")

print "Script executed successfully."

