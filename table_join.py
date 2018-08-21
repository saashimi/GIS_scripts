"""
table_join.py

Copy and paste this file into an active Python console within ArcGIS Desktop.
"""

import arcpy
import os

arcpy.env.overwriteOutput = True
arcpy.env.qualifedFieldNames = False

csvs = ['amstt_out', 'mdstt_out', 'amttime_out', 'mdttime_out']
scenarios = ['2015', '2027FC']
export_folder = os.path.join(os.getcwd(), 'joined_shp')

for scenario in scenarios:
    for csv in csvs:
        # We're loading the converted db files here.
        filename = '{0}_{1}.csv'.format(csv, scenario)
        shp = arcpy.AddJoin_management('taz2162', 'TAZ', filename, 'rTAZ')

        arcpy.FeatureClassToFeatureClass_conversion(
                shp,
                export_folder,
                '{0}_{1}.shp'.format(csv, scenario))

        arcpy.RemoveJoin_management(shp)
