'''****************************************************************************
Name:        GoogleAPI_TAZ_times.py 
Ping the Google API for an inter-TAZ travel time.  Use this for testing our 
travel model vs google times.URL for Google Distance Matrix API documentation:
https://developers.google.com/maps/documentation/distance-matrix/intro

Script queries a specific location from a feature class, and gets a travel time 
to the centroid of each TAZ.date used was calculated by entering date from
 https://www.epochconverter.com/

Script written by Al Mowbray, Metro
Ported to Python 2.7 by Kevin Saavedra
****************************************************************************'''

# Import system modules
from secrets import APIKEY
import arcpy
import time
import simplejson
import urllib

# INPUTS ----------------------------------------------------------------------
# set workspace and folder names here
arcpy.env.overwriteOutput = True
wd = 'M:\\plan\\trms\\staff\\saavedrak\\projects\\GIS_scripts\google_TAZ\\data\\'
# CHANGE TO WHERE YOU WANT TO WORK
arcpy.env.workspace = wd
taz = wd + 'taz_pt_w_coords.shp'
stations = wd + 'transfer_stations_w_TAZ.shp'
querytime = str(1546156800)
# midnight 12/30/2018 Pacific time, requires time in the future,
# # seconds since midnight 1/1/1970, UTC


def hms_string(sec_elapsed):
    # Sets up a timer
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def rows_as_update_dicts(cursor):
    # function to use column names as dictionary variables in a cursor
    colnames = cursor.fields
    for row in cursor:
        row_object = dict(zip(colnames, row))
        yield row_object
        cursor.updateRow([row_object[colname] for colname in colnames])


# PART 1 ----------------------------------------------------------------------
total_time = time.time()
start_time = time.time()
print("starting part 1...")

# first get the coordinates of the desired transfer station
fac_query = "FAC_NAME = 'Metro Central'"
arcpy.MakeFeatureLayer_management(stations, 'station_lyr', fac_query)
count = arcpy.GetCount_management('station_lyr')
printtext = "station layer has {} features.".format(count[0])
print(printtext)
field_names = [f.name for f in arcpy.ListFields('station_lyr')]
with arcpy.da.UpdateCursor('station_lyr', field_names) as sc:
    for row in rows_as_update_dicts(sc):
        station_xy = str(row['POINT_Y']) + "," + str(row['POINT_X'])

field_names = [f.name for f in arcpy.ListFields(taz)]
with arcpy.da.UpdateCursor(taz, field_names) as sc:
    for row in rows_as_update_dicts(sc):
        dest_xy = str(row['POINT_Y']) + "," + str(row['POINT_X'])
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        payload = "origins={0}&destinations={1}&mode=driving&language=en-EN&\
                   sensor=false&key={2}&departure_time={3}"\
                   .format(str(dest_xy), str(station_xy), APIKEY, querytime)
        url = url + payload
        result= simplejson.load(urllib.urlopen(url))
        driving_time = result['rows'][0]['elements'][0]['duration']['value']
        row['GOOGLE_TIME_FROM_CENTRAL'] = driving_time/60
        printtext = str(row['NO']) + ": dest desc = " + \
            result['destination_addresses'][0] + ", drive time = " + \
            str(round(driving_time/60)) + " min."
        print(printtext)
        # add a 1 second delay- google API will go all "DNS attack" at more
        # frequent requests...
        time.sleep(1)

end_time = time.time()
timetext = "Script complete! Total run time: {}".format(
    hms_string(end_time - total_time))
print(timetext)
