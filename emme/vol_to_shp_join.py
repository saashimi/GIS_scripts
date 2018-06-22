"""
Join volume CSV to ArcGIS Script.
By Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov

This script takes the output volume table of 
`peakSpreadAllDayVolumes_forGISJoin.py` and joins it to the `emme_links.shp`
file using the ArcGIS API.

The pathlib library is used for more elegant navigation of files in parent
folders.

This script is intended to be run from the model/peak/assignAllHours folder.
"""

import arcpy
import os
from pathlib import Path
import datetime as dt

def main():
    startTime = dt.datetime.now()
    print("Script run at {0}.".format(startTime))
    
    p = Path(__file__).parents[0]
    
    # `Scenario_1024` should be changed to the appropriate scenario number 
    # output by Emme.
    links_shapefile = os.path.join(str(p), 'New_Project', 'Media', 
                                           'Scenario_1024', 'emme_links.shp') 
    in_field = 'ID'
    join_table = os.path.join(str(p), 'volumes.csv')
    join_field = 'UNIQUEID'


    arcpy.TableToTable_conversion(join_table, str(p), 'volumes_converted.dbf' )
    converted_table = os.path.join(str(p), 'volumes_converted.dbf')

    
    joined_file = arcpy.JoinField_management(
                                            links_shapefile,
                                            in_field,
                                            converted_table,
                                            join_field)

    arcpy.FeatureClassToShapefile_conversion(joined_file, os.path.join(str(p)))
    
    endTime = dt.datetime.now()
    print("Script finished in {0}.".format(endTime - startTime))

if __name__ == '__main__':
    main()