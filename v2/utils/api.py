import json
import urllib.request as request

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
    Feeds the lat/long from GeoDB into the Climacell API.
    Returns a dictionary with different weather metrics (temp, dew pt, etc.).
    Results are updated hourly.
    Limit on API calls: 1000/day
    '''
    # set up headers
    headers = {}
    headers['apikey'] = 'dsZbfxJQ2fyXMLhnDJezjoeQJ77kiqSI'
    URL = 'https://api2.climacell.co/v2/weather/forecast/hourly?lat={}&lon={}'.format(latitude, longitude)
    result = access_info(URL, **headers)[0]
    return result

def return_historical_weather(latitude, longitude):
    '''
    Feeds the lat/long from GeoDB into the Historical Weather API.
    Returns a dictionary with different weather metrics (temp, dew pt, etc.).
    Limit on API calls: 500/day
    '''

    API_KEY = 'a7294c4e9c7e471aa64214148182711'
    # Provides weather data from 11/1 to 11/27
    URL = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx?format=json&q={},{}&date=2018-11-01&enddate=2018-11-27&key='.format(latitude, longitude)

    # Get to the weather data
    result = access_info(URL, API_KEY)['data']['weather'][0]
    return result

def return_zip_code(latitude, longitude):
    '''
    Feeds the lat/long from GeoDB into the Historical Weather API.
    Returns a dictionary with different weather metrics (temp, dew pt, etc.).
    Limit on API calls: 250/day
    '''
    API_KEY = 'Po9k2i9YAbWEjU5Kp0ey6J4ImKSKKAnrWVpXhRyPkt0CesMGE2Sw5TfATIwJ5OzF'
    URL = 'https://www.zipcodeapi.com/rest/{}/'.format(API_KEY)


if __name__ == '__main__':
    #print(return_weather(15,15))
    print(return_historical_weather(15,15))
