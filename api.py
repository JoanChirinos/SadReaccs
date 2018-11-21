def access_info(URL_STUB, API_KEY = None):
    '''
    Helper to access the info for a URL. Returns the JSON.
    Params: URL_STUB, API_KEY = None
    '''
    if API_KEY:
        URL = URL_STUB + API_KEY
    else:
        URL = URL_STUB
    response = request.urlopen(URL)
    response = response.read()
    info = json.loads(response)
    print(info)
    return info
