import json
import urllib.request as request
import datetime

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
    try:
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
    except:
        return 'Something broke'

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
    - 'humidity' (%): What the humidity is, returned as a list with 16 entries.

    NOTE: Index 0 contains the forecast for today
    '''
    try:
        # set up headers
        headers = {}
        headers['apikey'] = 'dsZbfxJQ2fyXMLhnDJezjoeQJ77kiqSI'
        fields= 'temp,feels_like,humidity,wind_speed,precipitation_accumulation'
        URL = 'https://api2.climacell.co/v2/weather/forecast/daily?lat={}&lon={}&fields={}'.format(latitude, longitude,fields)
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
            'humidity':[],
        }

        #set up dates
        date = datetime.datetime.now()
        days = 0

        #populate dict from result
        for item in result:
            # print('\nitem:',item['temp'][0]['observation_time'].split('T')[0])
            forecasts['date'].append((date + datetime.timedelta(days=days)).strftime('%Y-%m-%d'))
            days += 1
            forecasts['precipitation'].append(item['precipitation_accumulation']['value'])
            forecasts['temp']['min'].append(item['temp'][0]['min']['value'])
            forecasts['temp']['max'].append(item['temp'][1]['max']['value'])
            forecasts['feels_like']['min'].append(item['feels_like'][0]['min']['value'])
            forecasts['feels_like']['max'].append(item['feels_like'][1]['max']['value'])
            forecasts['wind_speed']['min'].append(item['wind_speed'][0]['min']['value'])
            forecasts['wind_speed']['max'].append(item['wind_speed'][1]['max']['value'])
            # average humidity
            average = (int(item['humidity'][0]['min']['value']) + int(item['humidity'][1]['max']['value']))/2
            forecasts['humidity'].append(average)

        return forecasts
    except:
        return 'Something broke'

def return_historical_weather(latitude, longitude):
    '''
    Feeds the lat/long from GeoDB into the Historical Weather API.
    Returns a dictionary with different weather metrics (temp, dew pt, etc.).
    Limit on API calls: 500/day

    Returns a dictionary with the accompanying data in this format:
    - 'date' (YYYY-MM-DD): The date, returned as a list with 16 entries.
    - 'temp' (C): The temperatures, returned as two nested dictionaries 'max' and 'min' containing lists of 16 entries each.
    - 'today': Data fields for today
        - NOTE: each hour interval is represented by a number in [0,7]; each number represents a dict with these keys:
            - 'precipitation': Precipitation recorded that hour
            - 'hour': Hour recorded
            - 'wind_speed': Wind speed recorded that hour
            - 'temp': Temp recorded that hour
            - 'weather_icon': How the sky looks visually that hour
            - 'weather_desc': Description of weather that hour
            - 'humidity' (%): Description of humidity that hour
    NOTE: Index len(date)-1 contains the forecast for today
    '''
    try:
        # set up dates
        date = datetime.datetime.now()
        todays_date = date.strftime('%Y-%m-%d')
        # go back a week and plug that date in as well
        last_week = date - datetime.timedelta(days=7)
        last_weeks_date = last_week.strftime('%Y-%m-%d')

        API_KEY = 'a7294c4e9c7e471aa64214148182711'
        # Provides weather data from 11/1 to 11/27
        URL = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx?format=json&q={},{}&date={}&enddate={}&key='.format(latitude, longitude, last_weeks_date, todays_date)

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
                0:{},
                1:{},
                2:{},
                3:{},
                4:{},
                5:{},
                6:{},
                7:{},
            },
        }

        hour_interval = 0
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
                    history['today'][hour_interval]['hour'] = hourly_item['time']
                    history['today'][hour_interval]['temp'] = hourly_item['tempC']
                    history['today'][hour_interval]['precipitation'] = hourly_item['precipMM']
                    history['today'][hour_interval]['wind_speed'] = hourly_item['windspeedKmph']
                    history['today'][hour_interval]['humidity'] = hourly_item['humidity']
                    history['today'][hour_interval]['weather_icon'] = hourly_item['weatherIconUrl'][0]['value']
                    history['today'][hour_interval]['weather_desc'] = hourly_item['weatherDesc'][0]['value']
                    hour_interval += 1

            history['precipitation'].append(precipitation)

        return history
    except:
        return 'Something broke'

if __name__ == '__main__':
    print(return_weather(48, 27))
    print(return_historical_weather(40,74))
