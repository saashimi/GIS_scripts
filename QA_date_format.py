"""
Handle dates in format:
MM/DD/YYYY HH:MM:SS AM/PM and convert to 

YYYY/MM/DD HH:MM:SS format
"""


fc = r'C:\Users\kev10076\Documents\ArcGIS\Projects\REST_migration\Rest_migration.gdb\Chicagot'
fields = ['Date', 'Date_st']

def date_time_handler(str_lst):
    date = str_lst[0].split('/')
    date_format = date[2] + '/' + date[0] + '/' + date[1]
    time = str_lst[1]
    AMPM = str_lst[2] 
    return date_format, time, AMPM

def date_handler(str_lst):
    date = str_lst[0].split('/')
    date_format = date[2] + '/' + date[0] + '/' + date[1]
    return date_format

with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        str_ = row[0].split(' ')
        if len(str_) > 2:
            d, t, a = date_time_handler(str_)
            row[1] = d + ' ' + t + ' ' + a
        else:
            d = date_handler(str_)
            row[1] = d
        cursor.updateRow(row)