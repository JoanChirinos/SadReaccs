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

def write_error(*args):
    '''
    Writes the error to a text file (ERROR_LOG.txt) if any of the API functions throw an error.
    Params: *args for taking in the error message and any supplementary information to log.
    '''
    f = open('../ERROR_LOG.txt', 'a')
    time_now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    f.write('START ERROR\ntime: {} UTC\n'.format(time_now))
    f.write('breakage info:\n')
    for arg in args:
        f.write('{}\n'.format(arg))
    f.write('END ERROR\n\n')
    f.close()

def search_city(query):
    '''
    Feeds the query through the Accuweather API and returns a result.
    Checks for trailing and leading whitespace and makes decisions accordingly.
    If stripping results in empty string, returns None.
    If no results are returned, returns an empty list.
    Limit on API calls: 50/day

    Returns a list. Each entry is a dictionary with the data in this format:
    - 'local_name': The local name of the city
    - 'eng_name': The English name of the city
    - 'region': The region/state of the city
    - 'country': The country of the city
    - 'latitude': Latitude of city
    - 'longitude': Longitude of city
    '''
    try:
        # remove both leading and trailing whitespace
        query = query.lstrip()
        query = query.rstrip()
        print(query)
        # check to see if the user was being a dud
        if query == '':
            return

        # replace all inner whitespace with %20 for API request
        query = query.replace(' ', '%20')

        # use the user's api key; if no key found, use a default
        file = open('../accuweather0.txt', 'r').read()
        apikey = file.strip()
        if apikey == '':
            return 'No API key found'

        # do the request
        URL = 'http://dataservice.accuweather.com/locations/v1/cities/search?q={}&apikey='.format(query)
        result = access_info(URL, apikey)

        #parse through the JSON and return the cities
        cities = []

        for item in result:
            cities.append({
                'local_name': item['LocalizedName'],
                'eng_name': item['EnglishName'],
                'region': item['AdministrativeArea']['EnglishName'],
                'country': item['Country']['EnglishName'],
                'latitude': item['GeoPosition']['Latitude'],
                'longitude': item['GeoPosition']['Longitude'],
            })

        return cities
    except Exception as error:
        write_error(error)
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
        # use the user's api key; if no key found, use a default
        file = open('../climacell.txt', 'r').read()
        apikey = file.strip()
        if apikey == '':
            return 'No API key found'

        # set up headers
        headers = {}
        headers['apikey'] = apikey

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
    except Exception as error:
        write_error(error)
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

        # use the user's api key; if no key found, use a default
        file = open('../worldweatheronline.txt', 'r').read()
        API_KEY = file.strip()
        if API_KEY == '':
            return 'No API key found'

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
    except Exception as error:
        write_error(error)
        return 'Something broke'

def return_random_dog():
    '''
    Returns a random image of a dog from the dog API.
    '''
    URL = 'https://dog.ceo/api/breeds/image/random'
    dog_pic = access_info(URL)['message']
    return dog_pic


if __name__ == '__main__':
    print(search_city('new york'))
    # print(return_weather(48, 27))
    # print(return_historical_weather(40,74))
    # print(return_random_dog())
