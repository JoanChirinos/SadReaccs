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
