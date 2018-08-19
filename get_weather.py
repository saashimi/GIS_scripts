# import the pretty print module, urllib2, and json
from pprint import pprint 
import urllib2
import json 

city = raw_input('Type the name of the city in which to obtain weather data.')
url1 = 'http://api.openweathermap.org/data/2.5/weather?q='
url2 = str(url1 + city)
json_obj = urllib2.urlopen(url2)
data = json.load(json_obj) # data is type 'dict'

#deg Fahrenheit data extraction
deg_C = data['main']['temp'] - 273 
deg_F = deg_C * 1.8 + 32
#Forecast High
degMax_C = data['main']['temp_max'] - 273
degMax_F = degMax_C * 1.8 + 32
#Forecast Low
degMin_C = data['main']['temp_min'] - 273
degMin_F = degMin_C * 1.8 + 32
# current weather
current_weather = data['weather'][0]['description']

#pprint(data)
print "The current temperature in " + city + " is " + str(deg_F) + " degrees Fahrenheit", "(" + str(deg_C) + " degrees Celsius)."
print "The recorded high today was " + str(degMax_F) + " degrees Fahrenheit."
print "The recorded low today was " + str(degMin_F) + " degrees Fahrenheit."
print "The current weather is " + str(current_weather) +"."
