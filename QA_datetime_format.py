"""
Handle dates in format:
MM/DD/YYYY HH:MM:SS AM/PM and convert to datetime format
"""
from datetime import datetime

fc = r'C:\Users\kev10076\Documents\ArcGIS\Projects\REST_migration\Output\hurricanes_sub4_102100.shp'
fields = ['iso_time', 'iso_dt']

with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        datestring = row[0]
        row[1] = datetime.strptime(datestring, '%m/%d/%Y %H:%M')
        cursor.updateRow(row)