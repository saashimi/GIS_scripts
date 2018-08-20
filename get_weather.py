"""
A Python script for prototype work.
"""

import requests
import requests_cache
from SECRETS import APIKEY


def request_data(city_in):
    payload = {'q': city_in, 'APPID': APIKEY}
    data = requests.get('https://api.openweathermap.org/data/2.5/forecast',
                        params=payload).json()
    return data


def temp_conversion(temp_k):
    temp_c = round(temp_k - 273.15)
    temp_f = round(temp_c * 1.8 + 32)
    return temp_c, temp_f


def main():
    # Local cache setup
    requests_cache.install_cache('owm_cache', expire_after=300)
    city = input('Type the name of the city in which to obtain weather '
                 'data. \n>>')
    data = request_data(city)

    # deg Fahrenheit data extraction
    data_index = data['list'][0]['main']
    # Current temp
    current_C, current_F = temp_conversion(data_index['temp'])
    # Forecast High
    deg_max_C, deg_max_F = temp_conversion(data_index['temp_max'])
    # Forecast Low
    deg_min_C, deg_min_F = temp_conversion(data_index['temp_min'])
    # current weather
    current_weather = data['list'][0]['weather'][0]['description']

    print('The recorded high today was {0} degrees Fahrenheit.'
          .format(str(deg_max_F)))

    print('The current temperature in {0} is {1} degrees Fahrenheit ({2} '
          'degrees Celsius).'.format(city, str(current_F), str(current_C)))

    print('The recorded low today was {0} degrees Fahrenheit.'
          .format(str(deg_min_F)))

    print('The current weather is {0}.'.format(str(current_weather)))


if __name__ == '__main__':
    main()
