"""
Join volume CSV to ArcGIS Script.
By Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov
"""

import arcpy
import os
from pathlib import Path

def main():
    # Go up TWO FOLDERS
    p = Path(__file__).parents[2]
    links_shapefile = os.path.join(str(p), 'New_Project', 'Media', 'emme_links.shp') 
    in_field = 'ID'
    join_table = os.path.join(str(p), 'volumes.csv')
    join_field = 'UNIQUEID'

    row_output = os.path.join(str(p), 'volumes_converted.csv')
    arcpy.CopyRows_management(join_table, row_output)
    
    joined_file = arcpy.JoinField_management(
                                            links_shapefile,
                                            in_field,
                                            row_output,
                                            join_field)

    arcpy.FeatureClassToShapefile_conversion(joined_file, 
                                                os.path.join(dirname, links_shapefile))
    

if __name__ == '__main__':
    main()