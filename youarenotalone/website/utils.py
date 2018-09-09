""" Get the lng / lat position of a city 
    Using Mapbox Geocoder """

from mapbox import Geocoder
import json

def searchLocation(cityName):
    """ get a list of city in france """
    geocoder = Geocoder(access_token = 'pk.eyJ1Ijoib3h5bzc4IiwiYSI6ImNqbGpuMTYzeTBkcXczcW4zaGZ1NjVsdnIifQ.feE4I_OmXTH-uwN5o8sIsw')
    response = geocoder.forward(cityName, country=['fr'])
    first = response.geojson()['features']
    return first

if __name__ == '__main__':
    result = json.dumps(searchLocation("Par"), indent=2, sort_keys=True)
    print(result)