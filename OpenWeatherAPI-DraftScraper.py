import json
import urllib.request

def api(): #Part of code taken from: https://straymarcs.net/2014/12/how-to-create-your-own-weather-forecast-program-using-python/
    api_key = '44b78ac274e9d94337e6620489fdcdbe' #Davy's Open Weather Map API Ky
    unit = 'metric'
    api = 'http://api.openweathermap.org/data/2.5/weather?lat=53.339983&lon=-6.295594' #St James Hospital #Replace the values of the altitude and longitude to accept other locations
    api_url = api + '&mode=json&units=' + unit + '&APPID=' + api_key
    return api_url

def request(api_url): #Part of code taken from: https://straymarcs.net/2014/12/how-to-create-your-own-weather-forecast-program-using-python/
    url = urllib.request.urlopen(api_url)
    output = url.read().decode('utf-8')
    api_data = json.loads(output)
    url.close()
    return api_data

def organised(api_data):
    data = dict(
        city=api_data.get('name'),
        country=api_data.get('sys').get('country'),
        temp=api_data.get('main').get('temp'),
        temp_max=api_data.get('main').get('temp_max'),
        temp_min=api_data.get('main').get('temp_min'),
        humidity=api_data.get('main').get('humidity'),
        pressure=api_data.get('main').get('pressure'),
        sky=api_data['weather'][0]['main'],
        dt=api_data.get('dt')
    )
    return data

def output(data):
    print('Current weather in: {}, {}:'.format(data['city'], data['country']))
    print(data['temp'], data['sky'])
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('Humidity: {}'.format(data['humidity']))
    print('Pressure: {}'.format(data['pressure']))

    print('Last update from the server: {}'.format(data['dt']))

if __name__ == '__main__': #Part of code taken from: https://straymarcs.net/2014/12/how-to-create-your-own-weather-forecast-program-using-python/
    output(organised(request(api())))
