"""
Join volume CSV to ArcGIS Script.
By Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov
"""

import arcpy
import os
from pathlib import Path
import datetime as dt

def main():
    # Go up TWO FOLDERS
    startTime = dt.datetime.now()
    print("Script run at {0}.".format(startTime))
    p = Path(__file__).parents[2]
    links_shapefile = os.path.join(str(p), 'New_Project', 'Media', 'emme_links.shp') 
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