"""
table_join.py

Copy and paste this file into an active Python console within ArcGIS Desktop.
Note: This script assumes that the CSVs to be joined to the TAZ shapefile 
have been imported to the local geodatabase.
"""

import arcpy
import os

arcpy.env.overwriteOutput = True

csvs = ['amstt_out', 'mdstt_out', 'amttime_out', 'mdttime_out']
scenarios = ['2015', '2027FC']
export_folder = os.path.join(os.getcwd(), 'joined_shp')

for scenario in scenarios:
    for csv in csvs:
        filename = '{0}_{1}'.format(csv, scenario)
        shp = arcpy.JoinField_management('taz2162', 'TAZ', filename, 'TAZ')

        arcpy.FeatureClassToFeatureClass_conversion(
                shp,
                export_folder,
                '{0}_{1}.shp'.format(csv, scenario))

        #arcpy.RemoveJoin_management(shp)
