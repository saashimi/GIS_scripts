mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "")[0]
sourceLayer = "C:/Users/kms22/Desktop/compy_desktop/data_holding/address_geocode/kd_symbology.lyr"

for lyr in arcpy.mapping.ListLayers(mxd, 'Full Time Students', df)[0]:
    arcpy.ApplySymbologyFromLayer_management(lyr, sourceLayer)