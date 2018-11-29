import json
import urllib.request as request
from datetime import date

def access_info(URL_STUB, API_KEY = None, **kwargs):
    '''
    Helper to access the info for a URL. Returns the JSON.
    Params: URL_STUB, API_KEY = None, **kwargs for applying headers to requests
    NOTE: API_KEY should only be used if the key can be put in the URL. Otherwise, use **kwargs.
    '''
    # if there's an API key that is not a header
    if API_KEY:
        URL = URL_STUB + API_KEY
    else:
        URL = URL_STUB
    request_object = request.Request(URL)
    # iterate through, adding headers if needed
    for key, value in kwargs.items():
        request_object.add_header(key, value)

    response = request.urlopen(request_object)
    response = response.read()
    info = json.loads(response)
    return info

def search_city(query):
    '''
    Feeds the query through the GeoDB API and returns a result.
    Checks for trailing and leading whitespace and makes decisions accordingly.
    If stripping results in empty string, returns None.
    If no results are returned, returns an empty list.
    Limit on API calls: 432k/day
    '''
    # remove both leading and trailing whitespace
    query = query.lstrip()
    query = query.rstrip()
    # print(query)
    # check to see if the user was being a dud
    if query == '':
        return
    # replace all inner whitespace with %20 for API request
    query = query.replace(' ', '%20')

    # set up headers
    headers = {}
    headers['X-Mashape-Key'] = 'tzSzy9eFlYmsh5iRSqqFq3dIdKanp19jDRIjsnaPw5zvVMWL5N'
    headers['X-Mashape-Host'] = 'wft-geo-db.p.mashape.com'

    # do the request
    URL = 'https://wft-geo-db.p.mashape.com/v1/geo/cities?namePrefix={}&offset=0&limit=10'.format(query)
    result = access_info(URL, **headers)['data']
    # return jsonify(result)
    return result

def return_weather(latitude, longitude):
    '''
    Feeds the lat/long from GeoDB into the Climacell API, which provides a 15-day forecast.
    Forecasts are updated hourly.
    Limit on API calls: 1000/day

    Returns a dictionary with the accompanying data in this format:
    - 'date' (YYYY-MM-DD): The date, returned as a list with 16 entries.
    - 'temp' (C): The temperatures, returned as two nested dictionaries 'max' and 'min' containing lists of 16 entries each.
    - 'precipitation' (mm): The precipitation, returned as a list with 16 entries.
    - 'feels_like' (C): What the temp feels like, returned as two nested dictionaries 'max' and 'min' containing lists of 16 entries each.
    - 'wind_speed' (m/s): What the wind speed is, returned as two nested dictionaries 'max' and 'min' containing lists of 16 entries each.
    - 'humidity' (%): What the humidity is, returned as two nested dictionaries 'max' and 'min' containing lists of 16 entries each.

    NOTE: Index 0 contains the forecast for today
    '''
    # set up headers
    headers = {}
    headers['apikey'] = 'dsZbfxJQ2fyXMLhnDJezjoeQJ77kiqSI'
    URL = 'https://api2.climacell.co/v2/weather/forecast/daily?lat={}&lon={}'.format(latitude, longitude)
    result = access_info(URL, **headers)

    # assemble dict
    forecasts = {
        'date':[],
        'precipitation':[],
        'temp':{
            'min':[],
            'max':[],
        },
        'feels_like':{
            'min':[],
            'max':[],
        },
        'wind_speed':{
            'min':[],
            'max':[],
        },
        'humidity':{
            'min':[],
            'max':[],
        }
    }

    #populate dict from result
    for item in result:
        # print('\nitem:',item['temp'][0]['observation_time'].split('T')[0])
        forecasts['date'].append(item['temp'][1]['observation_time'].split('T')[0])
        forecasts['precipitation'].append(item['precipitation_accumulation']['value'])
        forecasts['temp']['min'].append(item['temp'][0]['min']['value'])
        forecasts['temp']['max'].append(item['temp'][1]['max']['value'])
        forecasts['feels_like']['min'].append(item['feels_like'][0]['min']['value'])
        forecasts['feels_like']['max'].append(item['feels_like'][1]['max']['value'])
        forecasts['wind_speed']['min'].append(item['wind_speed'][0]['min']['value'])
        forecasts['wind_speed']['max'].append(item['wind_speed'][1]['max']['value'])
        forecasts['humidity']['min'].append(item['wind_speed'][0]['min']['value'])
        forecasts['humidity']['max'].append(item['wind_speed'][1]['max']['value'])

    return forecasts

def return_historical_weather(latitude, longitude):
    '''
    Feeds the lat/long from GeoDB into the Historical Weather API.
    Returns a dictionary with different weather metrics (temp, dew pt, etc.).
    Limit on API calls: 500/day

    Returns a dictionary with the accompanying data in this format:
    - 'date' (YYYY-MM-DD): The date, returned as a list with 16 entries.
    - 'temp' (C): The temperatures, returned as two nested dictionaries 'max' and 'min' containing lists of 16 entries each.
    - 'today': Data fields for today:
        - 'precipitation': List of precipitation by hour
        - 'hour': List of hours recorded
        - 'wind_speed': List of wind speeds recorded
        - 'temp': List of temps recorded
        - 'weather_icon': How the sky looks visually
        - 'weather_desc': Description of weather
        - 'humidity' (%): Description of humidity
    NOTE: Index len(date)-1 contains the forecast for today
    '''
    todays_date = str(date.today())
    API_KEY = 'a7294c4e9c7e471aa64214148182711'
    # Provides weather data from 11/1 to 11/27
    URL = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx?format=json&q={},{}&date=2018-11-20&enddate={}&key='.format(latitude, longitude, todays_date)

    # Get to the weather data
    result = access_info(URL, API_KEY)['data']['weather']

    # assemble dict
    history = {
        'date':[],
        'precipitation':[],
        'temp':{
            'min':[],
            'max':[],
        },
        'today':{
            'hours':[],
            'temp':[],
            'precipitation':[],
            'wind_speed':[],
            'weather_icon': [],
            'weather_desc':[],
            'humidity': [],
        },
    }

    # populate dict from result
    for item in result:
        history['date'].append(item['date'])
        history['temp']['max'].append(item['maxtempC'])
        history['temp']['min'].append(item['mintempC'])

        precipitation = 0
        # Tally up all the precipitation and insert it into history
        for hourly_item in item['hourly']:
            precipitation = round(precipitation + float(hourly_item['precipMM']),1)

            # For hour-by-hour weather data on today
            if item['date'] == todays_date:
                history['today']['hours'].append(hourly_item['time'])
                history['today']['temp'].append(hourly_item['tempC'])
                history['today']['precipitation'].append(hourly_item['precipMM'])
                history['today']['wind_speed'].append(hourly_item['windspeedKmph'])
                history['today']['humidity'].append(hourly_item['humidity'])
                history['today']['weather_icon'].append(hourly_item['weatherIconUrl'][0]['value'])
                history['today']['weather_desc'].append(hourly_item['weatherDesc'][0]['value'])

        history['precipitation'].append(precipitation)

    return history

if __name__ == '__main__':
    print(return_weather(15,15))
    print(return_historical_weather(40,74))
