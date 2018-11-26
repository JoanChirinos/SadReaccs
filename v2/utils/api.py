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
    '''
    # set up headers
    headers = {}
    headers['apikey'] = 'dsZbfxJQ2fyXMLhnDJezjoeQJ77kiqSI'
    URL = 'https://api2.climacell.co/v2/weather/forecast/hourly?lat={}&lon={}'.format(latitude, longitude)
    result = access_info(URL, **headers)[0]
    return result

if __name__ == '__main__':
    # print(return_weather(15,15))
