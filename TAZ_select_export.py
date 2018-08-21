"""
Select and export TAZ for client work.

By Kevin Saavedra, Metro, kevin.saavedra@oregonmetro.gov

Copy and paste this file into an active Python console within ArcGIS Desktop.
The .mxd should only be populated with the following shapefiles directly from
the geodatabase:
'AM_SOV_2015',
'AM_TRANSIT_2015',
'MD_SOV_2015',
'MD_TRANSIT_2015',
'AM_SOV_2027FC',
'AM_TRANSIT_2027FC',
'MD_SOV_2027FC',
'MD_TRANSIT_2027FC
"""

import arcpy
import os

arcpy.env.overwriteOutput = True

tazs = ['Legacy', 'OHSU', 'Providence', 'Project']
scenarios = ['AM_SOV_2015', 'AM_TRANSIT_2015', 'MD_SOV_2015',
             'MD_TRANSIT_2015', 'AM_SOV_2027FC', 'AM_TRANSIT_2027FC',
             'MD_SOV_2027FC', 'MD_TRANSIT_2027FC']
intervals = ['<=15', '<=30']

# os.setcwd('I:/ModServStaff/saavedra/misc/WashCo_Contours/')
export_folder = os.path.join(os.getcwd(), 'exports')

for scenario in scenarios:
    for taz in tazs:
        for interval in intervals:
            selection = arcpy.SelectLayerByAttribute_management(
                scenario,
                'NEW_SELECTION',
                '{0} {1}'
                .format(taz, interval))

            arcpy.AddField_management(
                selection,
                'site',
                'TEXT',
                field_length=16)

            with arcpy.da.UpdateCursor(selection, ['site']) as cursor:
                for row in cursor:
                    row[0] = taz
                    cursor.updateRow(row)

            # Export dissolved files:
            arcpy.Dissolve_management(
                selection,
                os.path.join(
                    export_folder,
                    "{0}{1}{2}{3}.shp".format(scenario, '_', taz, interval[2:])
                ),
                ['site'],
                '',
                'SINGLE_PART')

            # Export non-dissolved files:
            """
            arcpy.FeatureClassToFeatureClass_conversion(
                selection,
                export_folder,
                "{0}{1}{2}{3}.shp".format(scenario, "_", taz, interval[2:]))
            """
