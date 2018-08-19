"""
A Python2 script for prototype work.
Written for Python 2
"""

from pprint import pprint 
import requests
import requests_cache
from SECRETS import APIKEY 

city = raw_input('Type the name of the city in which to obtain weather data.')
payload = {'q': city, 'APPID': APIKEY}

requests_cache.install_cache('owm_cache', expire_after=300)
data = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=payload).json()

#deg Fahrenheit data extraction
deg_C = data['list'][0]['main']['temp'] - 273 
deg_F = deg_C * 1.8 + 32
#Forecast High
degMax_C = data['list'][0]['main']['temp_max'] - 273
degMax_F = degMax_C * 1.8 + 32
#Forecast Low
degMin_C = data['list'][0]['main']['temp_min'] - 273
degMin_F = degMin_C * 1.8 + 32
# current weather
current_weather = data['list'][0]['weather'][0]['description']


#pprint(data)
print "The current temperature in " + city + " is " + str(deg_F) + " degrees Fahrenheit", "(" + str(deg_C) + " degrees Celsius)."
print "The recorded high today was " + str(degMax_F) + " degrees Fahrenheit."
print "The recorded low today was " + str(degMin_F) + " degrees Fahrenheit."
print "The current weather is " + str(current_weather) +"."
